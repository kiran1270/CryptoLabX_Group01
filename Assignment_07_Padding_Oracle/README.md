# Assignment 07 - Padding Oracle Attack

## Student Information

- Group No.: 01
- Student ID: 2024UCP1270
- Assignment: 07
- Topic: Padding Oracle Attack

## Objective

To understand and demonstrate how a Padding Oracle Attack can recover
plaintext from an AES-CBC encrypted message without knowing the AES key.

## Concepts

The assignment demonstrates:

1. AES-CBC encryption
2. PKCS#7 padding
3. Padding oracle
4. Modification of previous ciphertext block
5. Plaintext recovery from right to left
6. Oracle query counting
7. Prevention of padding oracle vulnerabilities

## Attack

For CBC mode:

P(i) = D(C(i)) XOR C(i-1)

By modifying C(i-1), the attacker can influence the plaintext of C(i).

The padding oracle returns whether the resulting plaintext has valid
PKCS#7 padding.

The attack uses this information to recover plaintext one byte at a time.

## Important Constraint

The AES key is not provided to the attack function.

The attack uses only:

- IV
- Ciphertext
- Padding oracle

No ready-made padding-oracle attack library is used.

## Expected Result

The program successfully recovers:

Group01 ID2024UCP1270 Padding Oracle Attack Demonstration

and verifies that the recovered plaintext matches the original plaintext.

## Security Recommendation

A real system should not expose whether padding is valid or invalid.

Applications should use authenticated encryption such as AES-GCM or
ChaCha20-Poly1305.

If CBC encryption is used, authentication/MAC should be verified before
decryption and error responses should not reveal padding information.

## Files

- padding_oracle_attack.py
- README.md
- report.md
