import os
import subprocess

def esegui_comando_bin(comando):
    for nome_file in os.listdir():  
        if nome_file.endswith(".bin"):
            comando_completo = f"{comando} {nome_file}"
            try:
                subprocess.run(comando_completo, shell=True, check=True)
                print(f"Comando eseguito con successo per {nome_file}")
            except subprocess.CalledProcessError as e:
                print(f"Errore durante l'esecuzione del comando per {nome_file}: {e}")

comando_da_eseguire = "20070319exporterCP932"

esegui_comando_bin(comando_da_eseguire)