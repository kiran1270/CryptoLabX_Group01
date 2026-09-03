# Assignment 2 - SAST using Bandit

## Aim
To perform Static Application Security Testing on a Python program using Bandit.

## Tool
Bandit 1.6.2

## Description
Bandit is a static security analysis tool for Python programs. It scans source code
and identifies common security-related coding issues without executing the program.

## Experiment
A Python program containing intentional insecure coding practices was created and
analyzed using Bandit.

## Command Used
bandit -r program.py

## Findings
Total issues detected: 7
High severity: 5
Medium severity: 1
Low severity: 1
Confidence: High for all reported issues.

## Important Findings
B605 - os.system() may allow command injection.
B602 - subprocess with shell=True may allow command injection.
B303 - MD5 is an insecure hashing algorithm.
B404 - subprocess module usage requires security consideration.

## Result
Bandit successfully detected security issues in the test Python program.

## Conclusion
The experiment demonstrated how SAST can identify security weaknesses in source
code before program execution or deployment.
