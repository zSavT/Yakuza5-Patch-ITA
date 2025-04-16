"""
;==========================================
; Title:  packager.py
; Author: zSavT
; Date:   12/04/2025
;==========================================

Script per creare un archivio ZIP criptato (.pkg) di una cartella specificata.

Questo script richiede all'utente di fornire il percorso di una cartella,
il nome desiderato per il file di output criptato, e legge una chiave di
cifratura AES-256 da un file di testo chiamato 'chiave.txt' situato
nella stessa directory dello script.

Utilizza la libreria pyzipper per la creazione dell'archivio criptato.
"""

import os       # Per interazioni con il sistema operativo (path, walk, remove)
import pyzipper # La libreria principale per creare archivi ZIP criptati con AES
import sys      # Per terminare lo script in caso di errori critici (sys.exit)

# --- Costanti Globali ---
KEY_FILENAME = "chiave.txt"  # Nome del file che deve contenere la chiave di cifratura AES
                             # Questo file deve trovarsi nella stessa cartella dello script.

# --- Funzioni di Utilità ---

def get_input_path(prompt_msg):
    """
    Richiede all'utente di inserire un percorso e continua a chiederlo
    finché non viene fornito un percorso di directory valido.

    Args:
        prompt_msg (str): Il messaggio da mostrare all'utente come prompt.

    Returns:
        str: Il percorso della directory validato fornito dall'utente.
    """
    while True:
        path = input(prompt_msg).strip() # Legge l'input e rimuove spazi bianchi iniziali/finali
        if os.path.isdir(path): # Controlla se il percorso è una directory esistente
            return path
        print("❌ Percorso non valido o non è una directory. Riprova.")

def get_output_filename():
    """
    Richiede all'utente il nome base per il file di output e aggiunge
    l'estensione '.pkg'.

    Returns:
        str: Il nome completo del file di output (es. 'mio_archivio.pkg').
    """
    name = input("📦 Nome del file di output (senza estensione): ").strip()
    # Aggiunge l'estensione .pkg al nome fornito
    return f"{name}.pkg"

def confirm(prompt_msg):
    """
    Mostra un messaggio di conferma all'utente e attende una risposta 's' (sì).

    Args:
        prompt_msg (str): Il messaggio di conferma da visualizzare.

    Returns:
        bool: True se l'utente inserisce 's' (ignorando maiuscole/minuscole),
              False altrimenti.
    """
    # Converte l'input in minuscolo per il confronto
    return input(prompt_msg + " [s/N]: ").lower() == 's'

# --- Funzione Principale di Criptazione ---

def create_encrypted_package(source_folder, output_file, encryption_key):
    """
    Crea un archivio ZIP (.pkg) criptato utilizzando AES-256.

    Comprime i file della cartella sorgente in un file ZIP e lo cifra
    utilizzando la chiave fornita. Gestisce gli errori durante la creazione
    e tenta di rimuovere file parziali in caso di fallimento.

    Args:
        source_folder (str): Il percorso della cartella da archiviare e criptare.
        output_file (str): Il nome completo del file .pkg di output da creare.
        encryption_key (bytes): La chiave AES (come sequenza di byte) da usare
                                per la cifratura. Deve essere adatta per AES-256 (32 byte).
    """
    print(f"\n⚙️  Creazione pacchetto criptato in corso: {output_file}...")
    try:
        # Apre il file ZIP in modalità scrittura ('w') con pyzipper
        with pyzipper.AESZipFile(output_file, 'w',
                                 compression=pyzipper.ZIP_DEFLATED, # Algoritmo di compressione standard
                                 encryption=pyzipper.WZ_AES) as zf: # Specifica l'uso di AES
            # Imposta i dettagli della cifratura: AES a 256 bit
            zf.setencryption(pyzipper.WZ_AES, nbits=256)
            # Imposta la password (chiave) per la cifratura/decifratura
            zf.setpassword(encryption_key)

            # Itera ricorsivamente su tutti i file e sottocartelle della sorgente
            print("   Aggiunta file all'archivio:")
            for foldername, subfolders, filenames in os.walk(source_folder):
                for filename in filenames:
                    # Costruisce il percorso completo del file
                    filepath = os.path.join(foldername, filename)
                    # Calcola il percorso relativo rispetto alla cartella sorgente
                    # per mantenere la struttura delle cartelle nell'archivio
                    arcname = os.path.relpath(filepath, source_folder)
                    print(f"     -> {arcname}") # Mostra il file che viene aggiunto
                    # Scrive il file nell'archivio ZIP con il suo percorso relativo
                    zf.write(filepath, arcname)

        # Se tutto è andato a buon fine
        print(f"\n✅ Pacchetto criptato creato con successo: {output_file}")

    except Exception as e:
        # Gestisce eventuali errori durante la creazione del file ZIP
        print(f"\n❌ Errore critico durante la creazione del pacchetto: {e}")
        # Tenta di rimuovere il file .pkg parzialmente creato, se esiste
        if os.path.exists(output_file):
            try:
                os.remove(output_file)
                print(f"   🗑️  File parziale '{output_file}' rimosso.")
            except OSError as remove_error:
                # Errore durante la rimozione (es. permessi mancanti)
                print(f"   ⚠️  Impossibile rimuovere il file parziale '{output_file}': {remove_error}")
        # Esce dallo script indicando un errore
        sys.exit(1)


# --- Blocco di Esecuzione Principale ---
if __name__ == "__main__":
    """
    Punto di ingresso dello script. Gestisce il flusso principale:
    1. Lettura della chiave dal file.
    2. Raccolta input dall'utente (cartella sorgente, nome output).
    3. Visualizzazione riepilogo.
    4. Richiesta conferma.
    5. Avvio della creazione del pacchetto criptato.
    """
    print("\n🔐 Builder CLI per creare un pacchetto criptato")

    # --- 1. Lettura della chiave dal file ---
    aes_key_from_file = None # Inizializza la variabile della chiave
    print(f"   Lettura chiave dal file: '{KEY_FILENAME}'...")
    try:
        # Apre il file della chiave in modalità lettura ('r') con encoding UTF-8
        with open(KEY_FILENAME, 'r', encoding='utf-8') as f_key:
            # Legge la prima riga e rimuove spazi/newline circostanti
            key_str = f_key.readline().strip()

        # Controlla se la chiave letta è vuota
        if not key_str:
            print(f"❌ Errore: Il file della chiave '{KEY_FILENAME}' è vuoto.")
            sys.exit(1) # Termina se la chiave non è presente

        # Converte la stringa della chiave in bytes (richiesto da pyzipper)
        aes_key_from_file = key_str.encode('utf-8')

        # Controllo (opzionale ma raccomandato) sulla lunghezza della chiave
        # AES-256 richiede una chiave di 32 byte.
        key_len = len(aes_key_from_file)
        if key_len != 32:
            print(f"⚠️ Attenzione: La chiave nel file '{KEY_FILENAME}' è lunga {key_len} byte.")
            print("     Per AES-256 è raccomandata una chiave di 32 byte per la massima sicurezza.")
            # Nota: Lo script continuerà comunque, ma la sicurezza potrebbe essere compromessa
            # o pyzipper potrebbe sollevare un errore a seconda della sua implementazione interna.

    except FileNotFoundError:
        # Gestisce il caso in cui il file della chiave non esista
        print(f"❌ Errore: File della chiave '{KEY_FILENAME}' non trovato.")
        print(f"     Assicurati che il file esista nella stessa directory dello script")
        print(f"     e che contenga la chiave di cifratura sulla prima riga.")
        sys.exit(1) # Termina se il file chiave manca
    except Exception as e:
        # Gestisce altri possibili errori durante la lettura del file
        print(f"❌ Errore durante la lettura del file della chiave '{KEY_FILENAME}': {e}")
        sys.exit(1) # Termina per altri errori di lettura

    # --- 2. Raccolta input utente ---
    source = get_input_path("📁 Inserisci il percorso della cartella da includere nel pacchetto: ")
    output = "patch.pkg"

    # --- 3. Visualizzazione riepilogo ---
    print(f"\n📋 Riepilogo Operazione:")
    print(f"   - Cartella sorgente:    {source}")
    print(f"   - File pacchetto (.pkg):{output}")
    print(f"   - File chiave usato:    {KEY_FILENAME}") # Mostra quale file chiave è stato letto

    # --- 4. Richiesta Conferma ---
    # Chiede all'utente se vuole procedere con i parametri specificati
    if confirm("\nProcedere con la creazione del pacchetto criptato?"):
        # --- 5. Avvio Creazione Pacchetto ---
        # Chiama la funzione principale passando i parametri raccolti
        create_encrypted_package(source, output, aes_key_from_file)
    else:
        # Se l'utente non conferma
        print("\n⏹️  Operazione annullata dall'utente.")