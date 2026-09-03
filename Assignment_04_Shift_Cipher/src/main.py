from shift_cipher import encrypt, decrypt


print("===== Shift Cipher =====")

text = input("Enter text: ")
key = int(input("Enter key: "))

encrypted = encrypt(text, key)
decrypted = decrypt(encrypted, key)

print("Encrypted text:", encrypted)
print("Decrypted text:", decrypted)
