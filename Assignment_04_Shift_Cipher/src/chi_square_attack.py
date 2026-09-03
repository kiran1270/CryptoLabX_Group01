from shift_cipher import decrypt
from collections import Counter

ENGLISH_FREQ = {
    'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253,
    'e': 12.702, 'f': 2.228, 'g': 2.015, 'h': 6.094,
    'i': 6.966, 'j': 0.153, 'k': 0.772, 'l': 4.025,
    'm': 2.406, 'n': 6.749, 'o': 7.507, 'p': 1.929,
    'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056,
    'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150,
    'y': 1.974, 'z': 0.074
}

def chi_square(text):
    letters = [c.lower() for c in text if c.isalpha()]
    total = len(letters)

    if total == 0:
        return float("inf")

    counts = Counter(letters)
    score = 0

    for letter, expected_freq in ENGLISH_FREQ.items():
        expected = total * expected_freq / 100
        observed = counts.get(letter, 0)
        score += (observed - expected) ** 2 / expected

    return score


ciphertext = input("Enter ciphertext: ")

best_key = 0
best_score = float("inf")
best_text = ""

for key in range(26):
    text = decrypt(ciphertext, key)
    score = chi_square(text)

    if score < best_score:
        best_score = score
        best_key = key
        best_text = text

print("Predicted Key:", best_key)
print("Decrypted Text:", best_text)
print("Chi-Square Score:", round(best_score, 2))
