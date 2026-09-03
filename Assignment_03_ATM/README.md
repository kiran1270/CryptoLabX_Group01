# Assignment 3 - Secure Application Development

## Aim
To develop an ATM System with basic functionalities and identify security
vulnerabilities using static application security testing.

## Application
ATM System

## Core Functionalities
1. Login / PIN Verification
2. Balance Inquiry
3. Withdrawal
4. Deposit
5. PIN Change

## Security Testing
The application was analyzed using Bandit, a Python SAST tool.

Command used:
bandit -r atm.py

## Result
Bandit detected 5 security issues.
Severity: High
Confidence: High

The detected issues are related to insecure coding practices in the application.

## Test Cases
Test cases were prepared for valid PIN, invalid PIN, balance inquiry,
withdrawal, insufficient balance, deposit and PIN change.

## Conclusion
The ATM application was successfully developed and analyzed using a SAST
tool. The experiment helped in understanding common security weaknesses
and the importance of secure application development.
