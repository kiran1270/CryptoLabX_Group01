def encrypt(text, key):
    result = ""

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + key) % 26 + base)
        else:
            result += char

    return result


def decrypt(text, key):
    return encrypt(text, -key)


if __name__ == "__main__":
    text = input("Enter text: ")
    key = int(input("Enter key: "))

    encrypted = encrypt(text, key)
    decrypted = decrypt(encrypted, key)

    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)
