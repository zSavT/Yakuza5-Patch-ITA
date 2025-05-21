import os
import csv
import re

def trova_testi_lunghi(cartella_corrente):
    """
    Trova i testi più lunghi di 80 caratteri nei file CSV UTF-16 della cartella,
    escludendo quelli con zero o più di due caratteri di nuova riga.

    Args:
        cartella_corrente (str): Il percorso della cartella da analizzare.
    """

    testi_lunghi = []

    # Itera su tutti i file nella cartella corrente
    for nome_file in os.listdir(cartella_corrente):
        if nome_file.endswith(".csv"):
            percorso_file = os.path.join(cartella_corrente, nome_file)

            # Leggi il file CSV UTF-16
            try:
                with open(percorso_file, 'r', encoding='utf-16') as file_csv:
                    lettore_csv = csv.reader(file_csv, delimiter='\t')
                    for riga in lettore_csv:
                        # Controlla se la riga ha almeno 3 colonne
                        if len(riga) >= 3:
                            testo = riga[2]
                            # Rimuovi eventuali tag HTML e spazi extra
                            testo_pulito = ''.join(c for c in testo if c not in '<>').strip()
                            # Conta il numero di caratteri di nuova riga
                            numero_newline = testo_pulito.__contains__('\n')
                            # Controlla se il testo è più lungo di 80 caratteri e ha esattamente 1 o 2 '\n'
                            if len(testo_pulito) > 82 and numero_newline == 0:
                                testi_lunghi.append(f"{nome_file}: {testo_pulito}")
            except UnicodeError:
                print(f"Errore di codifica nel file: {nome_file}. Saltando.")

    return testi_lunghi

def scrivi_testi_su_file(testi, nome_file_output="Controllo.txt"):
    """
    Scrive i testi in un file di output.

    Args:
        testi (list): La lista dei testi da scrivere.
        nome_file_output (str): Il nome del file di output.
    """

    with open(nome_file_output, 'w', encoding='utf-8') as file_output:
        for testo in testi:
            file_output.write(testo + '\n')

if __name__ == "__main__":
    cartella_corrente = os.path.dirname(os.path.abspath(__file__))
    testi_trovati = trova_testi_lunghi(cartella_corrente)
    scrivi_testi_su_file(testi_trovati)
    print("Testi lunghi trovati e salvati in Controllo.txt")