# Assignment 07 - Padding Oracle Attack

## Group Number
Group 01

## Title
Padding Oracle Attack on AES-CBC

---

## Objective

The objective of this assignment is to understand and demonstrate
a Padding Oracle Attack on an AES-CBC encrypted message without
knowing the AES encryption key.

---

## Technologies Used

- Python 3
- AES
- AES-CBC
- PKCS#7 Padding
- PyCryptodome
- Ubuntu Linux
- Git and GitHub

---

## Attack Overview

A Padding Oracle Attack exploits a system that reveals whether the
padding of decrypted ciphertext is valid or invalid.

The attack works without directly knowing the AES key.

The attacker modifies the previous ciphertext block and sends the
modified ciphertext to the padding oracle.

The plaintext is recovered byte by byte from right to left.

---

## Encryption

The program first encrypts the following plaintext using AES-CBC:

Group01 Padding Oracle Attack Demonstration

PKCS#7 padding is applied before encryption.

---

## Padding Oracle

The padding oracle returns only two possible results:

- True - Valid PKCS#7 padding
- False - Invalid PKCS#7 padding

The AES key is not exposed to the attack function.

---

## Attack Process

1. Generate AES key and IV.
2. Encrypt the plaintext using AES-CBC.
3. Divide ciphertext into 16-byte blocks.
4. Modify the previous ciphertext block.
5. Try possible byte values from 0 to 255.
6. Query the padding oracle.
7. Recover plaintext bytes from right to left.
8. Recover all plaintext blocks.
9. Remove PKCS#7 padding.
10. Compare recovered plaintext with original plaintext.

---

## Important Formula

For AES-CBC:

P_i = D_K(C_i) XOR C_(i-1)

For the first block:

P_1 = D_K(C_1) XOR IV

---

## Files

```text
Assignment_07_Padding_Oracle/
│
├── padding_oracle_attack.py
├── README.md
└── report.md
