# ASSIGNMENT 07
# PADDING ORACLE ATTACK

## Student Details

**Group No.:** 01  
**Student ID:** 2024UCP1270  
**Assignment No.:** 07  
**Topic:** Padding Oracle Attack  

---

# 1. Aim

To understand and demonstrate how a Padding Oracle Attack can recover
plaintext from an AES-CBC encrypted message without knowing the
encryption key.

---

# 2. Objectives

1. Understand AES-CBC encryption.
2. Understand PKCS#7 padding.
3. Understand the role of a padding oracle.
4. Implement a padding oracle attack.
5. Recover plaintext without knowing the AES key.
6. Count the number of oracle queries.
7. Understand how to prevent padding oracle vulnerabilities.

---

# 3. Software and Requirements

- Ubuntu / Ubuntu WSL
- Python 3
- PyCryptodome
- Git
- GitHub

---

# 4. Theory

## 4.1 AES-CBC

AES is a symmetric block cipher with a block size of 128 bits
(16 bytes).

In CBC mode, every plaintext block is XORed with the previous
ciphertext block before encryption.

For the first block, the IV is used.

Encryption:

C1 = AES_Encrypt(P1 XOR IV)

C2 = AES_Encrypt(P2 XOR C1)

Decryption:

P1 = AES_Decrypt(C1) XOR IV

P2 = AES_Decrypt(C2) XOR C1

---

## 4.2 PKCS#7 Padding

AES works on blocks of 16 bytes. If the plaintext is not a multiple
of 16 bytes, PKCS#7 padding is added.

For example, if 3 bytes of padding are required:

03 03 03

The last byte specifies the padding length.

---

## 4.3 Padding Oracle

A padding oracle is a function that reveals whether decrypted
ciphertext contains valid PKCS#7 padding.

It returns:

- True: valid padding
- False: invalid padding

The attacker uses this information to recover plaintext.

---

# 5. Padding Oracle Attack

CBC decryption is:

P(i) = D(C(i)) XOR C(i-1)

The attacker modifies the previous ciphertext block C(i-1).

This changes the plaintext of the target block.

The attacker tries different byte values and sends the modified
ciphertext to the oracle.

When the oracle reports valid padding, the attacker obtains
information about the plaintext byte.

The process is performed from:

RIGHT → LEFT

until the entire plaintext block is recovered.

The same process is repeated for all ciphertext blocks.

---

# 6. Implementation

The program was implemented in Python using PyCryptodome.

The attack does not receive or access the AES key.

The oracle internally performs AES-CBC decryption and only exposes
whether the padding is valid.

The program does not use a ready-made padding-oracle attack library.

---

# 7. Terminal Commands

```bash
cd ~/CryptoLabX_Group01

mkdir -p Assignment_07_Padding_Oracle

cd Assignment_07_Padding_Oracle

python3 -m venv venv

source venv/bin/activate

pip install pycryptodome

gedit padding_oracle_attack.py

python3 padding_oracle_attack.py
