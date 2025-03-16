import datetime

def main():
    output_file = "test/output.txt"

    # Scrive la data e ora correnti nel file, così cambia ad ogni run
    with open(output_file, "w") as f:
        current_time = datetime.datetime.now().isoformat()
        f.write(f"Updated at: {current_time}\n")
        print(f"Wrote to {output_file}: Updated at {current_time}")

if __name__ == "__main__":
    main()
