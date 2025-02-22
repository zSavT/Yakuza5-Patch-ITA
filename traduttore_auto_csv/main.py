import csv
import os
import re
import time
from deep_translator import GoogleTranslator

def traduci_testo_csv(input_file, output_file, source_lang='en', target_lang='it'):
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    
    righe_originali = 0
    righe_tradotte = 0
    
    with open(input_file, 'r', encoding='utf-16') as infile, open(output_file, 'w', encoding='utf-16', newline='') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        for row in reader:
            if not row:
                writer.writerow([])  # Mantieni righe vuote
                continue
            
            righe_originali += 1
            translated_row = []
            original_row = []  # Per memorizzare i valori originali separati
            
            # Variabile per gestire i casi di testo diviso su più colonne
            combined_text = ''
            combined_original = []

            for value in row:
                if value.isdigit() or re.match(r'^[\W_]+$', value) or "\\u" in value: 
                    if combined_text:  # Se c'era un testo combinato, traduciamolo e aggiungiamolo
                        try:
                            translated_text = translator.translate(combined_text).replace("\n", "\\n").replace("<Corsivo>", "<Italic>").replace("</Corsivo>", "</Italic>")
                            translated_row.append(translated_text)
                            original_row.append(' '.join(combined_original))  # Unisce le frasi originali
                        except Exception as e:
                            print(f"Errore nella traduzione di '{combined_text}': {e}")
                            translated_row.append(combined_text)
                            original_row.append(' '.join(combined_original))
                        
                        # Reset per la prossima sequenza di testo
                        combined_text = ''
                        combined_original = []

                    translated_row.append(value)
                    original_row.append(value)
                else:
                    # Se non è un numero o un carattere speciale, combinare il testo
                    combined_text += ' ' + value if combined_text else value
                    combined_original.append(value)
            
            # Gestisci l'ultimo caso in cui c'è testo combinato ma non è stato tradotto
            if combined_text:
                try:
                    translated_text = translator.translate(combined_text).replace("\n", "\\n").replace("<Corsivo>", "<Italic>").replace("</Corsivo>", "</Italic>")
                    translated_row.append(translated_text)
                    original_row.append(' '.join(combined_original))
                except Exception as e:
                    print(f"Errore nella traduzione di '{combined_text}': {e}")
                    translated_row.append(combined_text)
                    original_row.append(' '.join(combined_original))
            
            print(f"\033[33mOriginale: {', '.join(original_row)}\033[0m")
            print(f"\033[32mTradotto: {', '.join(translated_row)}\033[0m")
            
            writer.writerow(translated_row)
            righe_tradotte += 1

    print(f"Numero di righe originali: {righe_originali}")
    print(f"Numero di righe tradotte: {righe_tradotte}", "\n")

def traduci_tutti_csv_in_cartella(cartella, output_cartella, source_lang='en', target_lang='it'):
    start_time = time.time()
    
    if not os.path.exists(output_cartella):
        os.makedirs(output_cartella)

    for filename in os.listdir(cartella):
        if filename.endswith('.csv'):
            input_file = os.path.join(cartella, filename)
            output_file = os.path.join(output_cartella, filename)
            
            print(f"Traducendo {filename}...")
            traduci_testo_csv(input_file, output_file, source_lang, target_lang)
            print(f"File tradotto salvato come: {output_file}")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print(f"Tempo totale di esecuzione: {int(hours)}h {int(minutes)}m {int(seconds)}s")

if __name__ == "__main__":
    cartella = "input"  # Cartella contenente i file CSV di input
    output_cartella = os.path.join(cartella, "tradotto")  # Sottocartella per i file tradotti

    traduci_tutti_csv_in_cartella(cartella, output_cartella)
    print("Traduzione completata per tutti i file CSV.")
