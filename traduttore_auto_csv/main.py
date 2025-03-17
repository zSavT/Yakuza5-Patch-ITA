import time
import google.generativeai as genai
import csv
import os
import re
import argparse
import itertools
import sys

def get_api_key():
    parser = argparse.ArgumentParser(description="Script per tradurre file CSV utilizzando Google Gemini.")
    parser.add_argument("--api", type=str, help="Specifica la chiave API per Google Gemini. In alternativa, creare un file 'api_key.txt' nella stessa cartella contenente la chiave API.")
    args = parser.parse_args()
    
    if args.api:
        print("✅ API key fornita tramite flag --api")
        return args.api
    
    api_key_file = "api_key.txt"
    if os.path.exists(api_key_file):
        with open(api_key_file, "r") as f:
            print("✅ API key caricata con successo dal file api_key.txt")
            return f.read().strip()
    
    print("❌ Errore: Chiave API non trovata. Creare un file 'api_key.txt' nella stessa cartella dello script con la chiave API o specificarla con il flag --api.")
    raise ValueError("Chiave API non trovata.")

api_key = get_api_key()
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

def animazione_caricamento(stop_event):
    for simbolo in itertools.cycle(['|', '/', '-', '\\']):
        if stop_event.is_set():
            break
        sys.stdout.write(f"\r🔄 Traduzione in corso {simbolo} ")
        sys.stdout.flush()
        time.sleep(0.2)
    sys.stdout.write("\r")

def traduci_testo_csv(input_file, output_file):
    from threading import Thread, Event
    stop_event = Event()
    loader_thread = Thread(target=animazione_caricamento, args=(stop_event,))
    loader_thread.start()

    righe_originali = 0
    righe_tradotte = 0

    with open(input_file, 'r', encoding='utf-16') as infile, open(output_file, 'w', encoding='utf-16', newline='') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        for row in reader:
            if not row:
                writer.writerow([])
                continue

            righe_originali += 1
            translated_row = row[:]

            if len(row) > 2 and isinstance(row[2], str) and row[2].strip():
                value = row[2]
                if value == '' or value.isdigit() or re.match(r'^[\W_]+$', value) or "\\u" in value or value == " ":
                    pass
                else:
                    while True:  # CICLO INFINITO FINCHÉ NON RIESCE
                        try:
                            prompt = f"""Ti passerò del testo proveniente da un file csv del gioco Yakuza 4 contenente i dialoghi del gioco e devi tradurmi il testo in italiano considerando le tematiche e linguaggio del gioco, ma solo il testo, i restanti codici html, numeri, 
                            devono rimanere invariati. Limitati a rispondere solamente con la traduzione, senza aggiungere tuoi commenti personali. 
                            Se ti chiedo di tradurre \"Thanks\", non devi ringraziarmi, ma tradurre e basta. Ora ti mando il testo da tradurre: {value}"""

                            time.sleep(2)  # Delay tra richieste (puoi anche alzarlo se serve)
                            response = model.generate_content(prompt)
                            translated_text = response.text.strip()
                            translated_text = translated_text.replace("<Corsivo>", "<Italic>").replace("</Corsivo>", "</Italic>")

                            translated_row[2] = translated_text
                            print(f"\n🇬🇧 Testo originale: {value}")
                            print(f"🇮🇹 Testo tradotto: {translated_text}")
                            print(f"Lista token traduzione: {translated_row}")
                            break  # SE TUTTO VA BENE, ESCI DAL WHILE
                        except Exception as e:
                            print(f"❌ Errore nella traduzione di '{value}': {e}")
                            print("⏳ Riprovo tra 20 secondi...")
                            time.sleep(20)


            writer.writerow(translated_row)
            righe_tradotte += 1

    stop_event.set()
    loader_thread.join()
    print(f"✅ Numero di righe originali: {righe_originali}")
    print(f"✅ Numero di righe tradotte: {righe_tradotte}\n")

def traduci_tutti_csv_in_cartella(cartella, output_cartella):
    start_time = time.time()

    if not os.path.exists(output_cartella):
        os.makedirs(output_cartella)

    for filename in os.listdir(cartella):
        if filename.endswith('.csv'):
            input_file = os.path.join(cartella, filename)
            output_file = os.path.join(output_cartella, filename)

            print(f"📂 Traducendo {filename}...")
            traduci_testo_csv(input_file, output_file)
            print(f"✅ File tradotto salvato come: {output_file}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print(f"⏳ Tempo totale di esecuzione: {int(hours)}h {int(minutes)}m {int(seconds)}s")
    print(cartella)
    print(output_cartella)

if __name__ == "__main__":
    cartella = "input"
    output_cartella = os.path.join(cartella, "tradotto")

    traduci_tutti_csv_in_cartella(cartella, output_cartella)
    print("🎉 Traduzione completata per tutti i file CSV.")
