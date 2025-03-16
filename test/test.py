# path/to/your_script.py

def main():
    input_file = "input.txt"
    output_file = "output.csv"

    # Legge l'input file (contenuto ignorato per questo test)
    try:
        with open(input_file, "r") as f:
            content = f.read()
            print(f"Letto contenuto da {input_file}:")
            print(content)
    except FileNotFoundError:
        print(f"{input_file} non trovato. Crealo con del testo di prova.")
        return

    # Scrive il file di output con la parola 'test'
    with open(output_file, "w") as f:
        f.write("test\n")
        print(f"Scritto 'test' in {output_file}")

if __name__ == "__main__":
    main()
