from shift_cipher import decrypt

def load_words():
    with open("dictionary/english_words.txt", "r") as file:
        return set(word.strip().lower() for word in file if word.strip())

ciphertext = input("Enter ciphertext: ")
words = load_words()

best_key = 0
best_score = -1
best_text = ""

for key in range(26):
    text = decrypt(ciphertext, key)
    score = sum(1 for word in text.lower().split() if word in words)

    if score > best_score:
        best_score = score
        best_key = key
        best_text = text

print("Predicted Key:", best_key)
print("Decrypted Text:", best_text)
print("Dictionary Score:", best_score)
