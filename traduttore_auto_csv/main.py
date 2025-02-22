"""
File: main.py
Author: SavT
Date: 17/01/2025
"""

import csv
import os
from deep_translator import GoogleTranslator


def traduci_testo_csv(input_file, output_file, source_lang='en', target_lang='it'):

    translator = GoogleTranslator(source=source_lang, target=target_lang)

    with (open(input_file, 'r', encoding='utf-16') as infile, open(output_file, 'w', encoding='utf-16',
                                                                  newline='') as outfile):
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        for row in reader:
            if len(row) < 3:
                continue  # Salta righe malformattate
            start, end, text = row
            try:
                text = text.replace("\\n", "\n") # La lib della traduzione tende ad eliminare \n, in questo modo si raggira
                tradotto = translator.translate(text).replace("\n", "\\n"
                                                              ).replace("<Corsivo>","<Italic>").replace("</Corsivo>", "</Italic>") # La lib traduce letteralmente anche i tag ogni tanto
                writer.writerow([start, end, tradotto])
            except Exception as e:
                print(f"Errore nella traduzione di '{text}': {e}")
                writer.writerow([start, end, text])  # Mantieni il testo originale in caso di errore


def traduci_tutti_csv_in_cartella(cartella, output_cartella, source_lang='en', target_lang='it'):

    if not os.path.exists(output_cartella):
        os.makedirs(output_cartella)

    for filename in os.listdir(cartella):
        if filename.endswith('.csv'):
            input_file = os.path.join(cartella, filename)
            output_file = os.path.join(output_cartella, filename)

            print(f"Traducendo {filename}...")
            traduci_testo_csv(input_file, output_file, source_lang, target_lang)
            print(f"File tradotto salvato come: {output_file}")


if __name__ == "__main__":
    cartella = "input"  # Cartella contenente i file CSV di input
    output_cartella = os.path.join(cartella, "tradotto")  # Sottocartella per i file tradotti

    traduci_tutti_csv_in_cartella(cartella, output_cartella)
    print("Traduzione completata per tutti i file CSV.")
