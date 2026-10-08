# Assignment 07 - Padding Oracle Attack

## Group Number
Group 01

## Objective

To understand and demonstrate a Padding Oracle Attack on an
AES-CBC encrypted message without knowing the AES encryption key.

## Technologies Used

- Python 3
- AES-CBC
- PKCS#7
- PyCryptodome
- Ubuntu
- GitHub

## Background

AES-CBC encrypts plaintext in blocks. PKCS#7 padding is added when
the plaintext is smaller than a complete AES block.

A padding oracle is a system that tells whether decrypted ciphertext
contains valid or invalid padding.

## Attack

The attack modifies the previous ciphertext block and sends the
modified ciphertext to the oracle.

The attack starts from the rightmost byte and proceeds towards the
left.

The attacker tries different byte values and uses the oracle's
valid/invalid response to recover plaintext.

The AES key is not used by the attack function.

## Test Plaintext

Group01 Padding Oracle Attack Demonstration

## Result

The attack successfully recovered the original plaintext.

Recovered Plaintext:

Group01 Padding Oracle Attack Demonstration

Verification:

SUCCESS - Plaintext recovered correctly.

The program also counts and displays the number of oracle queries.

## Security Recommendation

Padding oracle attacks can be prevented by:

1. Using authenticated encryption such as AES-GCM.
2. Avoiding detailed padding error messages.
3. Using generic error responses.
4. Authenticating ciphertext before decryption where applicable.

## Screenshots

### 1. Environment Setup

[PASTE SCREENSHOT HERE]

### 2. Attack Code

[PASTE SCREENSHOT HERE]

### 3. Program Output

[PASTE SCREENSHOT HERE]

### 4. Git Status

[PASTE SCREENSHOT HERE]

### 5. GitHub Repository

[PASTE SCREENSHOT HERE]

## Conclusion

The experiment demonstrated that improper handling of padding errors
in AES-CBC can allow an attacker to recover plaintext without knowing
the encryption key.
