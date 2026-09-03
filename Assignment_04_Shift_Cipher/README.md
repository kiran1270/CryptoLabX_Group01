# Assignment 4 - Cryptanalysis of Shift Cipher

## Aim
To perform cryptanalysis of a Shift Cipher using Brute Force,
Dictionary Scoring and Chi-Square Analysis.

## Methods
1. Brute Force
2. Dictionary Scoring
3. Chi-Square Analysis

## Brute Force
All 26 possible keys are tested and the corresponding plaintexts
are displayed.

## Dictionary Scoring
Each decrypted candidate is compared with an English word list.
The key with the highest dictionary score is selected.

For KHOOR ZRUOG:
Predicted Key = 3
Plaintext = HELLO WORLD

## Chi-Square Analysis
The frequency distribution of each decrypted candidate is compared
with standard English letter frequencies. The candidate with the
lowest Chi-Square score is selected.

For very short ciphertext, frequency analysis may give an incorrect
key because there is insufficient statistical information.

## Comparison
Dictionary Scoring correctly predicted key 3 for the test ciphertext.
Chi-Square analysis demonstrated the limitation of using frequency
analysis on very short text.

## Conclusion
The experiment demonstrated three approaches to Shift Cipher
cryptanalysis and showed the importance of ciphertext length and
English-language statistics in cryptanalysis.
