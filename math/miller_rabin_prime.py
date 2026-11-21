import secrets
import time
from math import gcd

try:
    from sympy import isprime
except ImportError:
    isprime = None


BIT_LENGTH = 512

# Miller-Rabin bases / rounds
BASES = [
    2, 3, 5, 7, 11,
    13, 17, 19, 23, 29,
    31, 37, 41, 43, 47,
    53, 59, 61, 67, 71
]


def generate_candidate(bits):
    """
    Generate an odd integer having exactly 'bits' bits.
    """
    candidate = secrets.randbits(bits)

    # Set the most significant bit to guarantee exact bit length
    candidate |= (1 << (bits - 1))

    # Set the least significant bit to make candidate odd
    candidate |= 1

    return candidate


def miller_rabin(n, bases):
    """
    Miller-Rabin primality test.
    Returns True if n passes all supplied bases.
    """

    if n < 2:
        return False

    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

    if n in small_primes:
        return True

    for p in small_primes:
        if n % p == 0:
            return False

    # Write n - 1 = 2^s * d
    d = n - 1
    s = 0

    while d % 2 == 0:
        s += 1
        d //= 2

    for base in bases:

        if base >= n:
            continue

        if gcd(base, n) != 1:
            return False

        x = pow(base, d, n)

        if x == 1 or x == n - 1:
            continue

        passed = False

        for _ in range(s - 1):
            x = pow(x, 2, n)

            if x == n - 1:
                passed = True
                break

        if not passed:
            return False

    return True


def check_each_base(n, bases):
    """
    Check and display result for every Miller-Rabin base.
    """

    print("\nMiller-Rabin Base Verification:")

    d = n - 1
    s = 0

    while d % 2 == 0:
        s += 1
        d //= 2

    all_passed = True

    for base in bases:

        if base >= n:
            print(f"Base {base}: PASS")
            continue

        if gcd(base, n) != 1:
            print(f"Base {base}: FAIL")
            all_passed = False
            continue

        x = pow(base, d, n)

        if x == 1 or x == n - 1:
            print(f"Base {base}: PASS")
            continue

        passed = False

        for _ in range(s - 1):
            x = pow(x, 2, n)

            if x == n - 1:
                passed = True
                break

        if passed:
            print(f"Base {base}: PASS")
        else:
            print(f"Base {base}: FAIL")
            all_passed = False

    return all_passed


def main():

    print("=" * 60)
    print("512-BIT PRIME GENERATION USING MILLER-RABIN")
    print("=" * 60)

    print(f"\nAssigned Bit Length : {BIT_LENGTH}")
    print(f"Miller-Rabin Rounds : {len(BASES)}")
    print(f"Bases               : {BASES}")

    candidates_tested = 0

    start_time = time.perf_counter()

    while True:

        candidate = generate_candidate(BIT_LENGTH)

        candidates_tested += 1

        print(f"\nTesting Candidate #{candidates_tested}")
        print(f"Candidate: {candidate}")

        if miller_rabin(candidate, BASES):
            prime_candidate = candidate
            break

        print("Result: Candidate FAILED Miller-Rabin test.")

    end_time = time.perf_counter()

    execution_time = end_time - start_time

    actual_bit_length = prime_candidate.bit_length()

    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)

    print(f"\nGenerated Prime Candidate:")
    print(prime_candidate)

    print(f"\nActual Bit Length: {actual_bit_length}")

    print(f"Candidates Tested: {candidates_tested}")

    print(f"Miller-Rabin Rounds: {len(BASES)}")

    print(f"Total Execution Time: {execution_time:.6f} seconds")

    # Verification of exact bit length
    print("\nBit Length Verification:")

    if actual_bit_length == BIT_LENGTH:
        print("PASS - Candidate has exactly 512 bits.")
    else:
        print("FAIL - Candidate does not have 512 bits.")

    # Verify every Miller-Rabin base
    bases_passed = check_each_base(prime_candidate, BASES)

    if bases_passed:
        print("\nPASS - Candidate passed all Miller-Rabin bases.")
    else:
        print("\nFAIL - Candidate failed Miller-Rabin verification.")

    # Independent verification using SymPy
    print("\nIndependent Primality Verification:")

    if isprime is not None:

        independent_result = isprime(prime_candidate)

        if independent_result:
            print("PASS - SymPy independently verified the number as prime.")
        else:
            print("FAIL - SymPy did not verify the number as prime.")

    else:
        print("SymPy is not installed.")
        independent_result = None

    # Save experimental results
    output_file = "outputs/miller_rabin_results.txt"

    with open(output_file, "w") as file:

        file.write("CRYPTOLABX - MILLER-RABIN PRIME GENERATION\n")
        file.write("=" * 60 + "\n\n")

        file.write("Experimental Results\n")
        file.write("-" * 60 + "\n")

        file.write(f"Assigned Bit Length: {BIT_LENGTH}\n")
        file.write(f"Generated Prime Candidate: {prime_candidate}\n")
        file.write(f"Actual Bit Length: {actual_bit_length}\n")
        file.write(f"Number of Candidates Tested: {candidates_tested}\n")
        file.write(f"Number of Miller-Rabin Rounds: {len(BASES)}\n")
        file.write(f"Total Execution Time: {execution_time:.6f} seconds\n\n")

        file.write("Miller-Rabin Bases\n")
        file.write("-" * 60 + "\n")

        for base in BASES:
            file.write(f"Base {base}: PASS\n")

        file.write("\nVerification\n")
        file.write("-" * 60 + "\n")

        if actual_bit_length == BIT_LENGTH:
            file.write("Bit Length Verification: PASS\n")
        else:
            file.write("Bit Length Verification: FAIL\n")

        if bases_passed:
            file.write("Miller-Rabin Verification: PASS\n")
        else:
            file.write("Miller-Rabin Verification: FAIL\n")

        if independent_result is True:
            file.write("Independent SymPy Verification: PASS\n")
        elif independent_result is False:
            file.write("Independent SymPy Verification: FAIL\n")
        else:
            file.write("Independent SymPy Verification: NOT AVAILABLE\n")

    print(f"\nResults saved to: {output_file}")

    print("\n" + "=" * 60)
    print("PROGRAM COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
