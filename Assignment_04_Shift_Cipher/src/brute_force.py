from shift_cipher import decrypt

ciphertext = input("Enter ciphertext: ")

print("\nAll possible decryptions:")
for key in range(26):
    print(f"Key {key:2}: {decrypt(ciphertext, key)}")
