import os
from datetime import datetime
from collections import Counter

LOG_FILE = "cryptolabx.log"


def log_action(option):
    with open(LOG_FILE, "a") as file:
        file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {option}\n")


def analyze_file():
    files = [f for f in os.listdir("datasets") if f.endswith(".txt")]

    if not files:
        print("No text files found in datasets folder.")
        return

    print("\nAvailable Files:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")

    try:
        choice = int(input("Select file: "))
        filename = files[choice - 1]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return

    with open(os.path.join("datasets", filename), "r") as file:
        text = file.read()

    characters = len(text)
    words = len(text.split())
    lines = len(text.splitlines())
    unique_characters = len(set(text))

    frequency = Counter(c.lower() for c in text if c.isalpha())

    print("\n===== File Analysis =====")
    print("File:", filename)
    print("Characters:", characters)
    print("Words:", words)
    print("Lines:", lines)
    print("Unique Characters:", unique_characters)

    print("\nLetter Frequency:")
    for letter, count in sorted(frequency.items()):
        print(f"{letter} : {count}")


def main():
    while True:
        print("\n===== CryptoLabX Toolkit =====")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Attack")
        print("4. Analyze")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            log_action("Encrypt selected")
            print("Encryption module - Coming Soon")

        elif choice == "2":
            log_action("Decrypt selected")
            print("Decryption module - Coming Soon")

        elif choice == "3":
            log_action("Attack selected")
            print("Attack module - Coming Soon")

        elif choice == "4":
            log_action("Analyze selected")
            analyze_file()

        elif choice == "5":
            log_action("Exit selected")
            print("Exiting CryptoLabX...")
            break

        else:
            log_action("Invalid option selected")
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
