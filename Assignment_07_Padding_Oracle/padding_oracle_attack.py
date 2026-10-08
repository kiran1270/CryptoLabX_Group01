from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


# ============================================================
# ASSIGNMENT 07 - PADDING ORACLE ATTACK
# ============================================================

BLOCK_SIZE = 16


# ------------------------------------------------------------
# Secret AES key
# The attack function NEVER accesses this key.
# ------------------------------------------------------------
SECRET_KEY = get_random_bytes(16)


# ------------------------------------------------------------
# Encryption
# ------------------------------------------------------------
def encrypt_message(plaintext):
    iv = get_random_bytes(BLOCK_SIZE)

    cipher = AES.new(
        SECRET_KEY,
        AES.MODE_CBC,
        iv
    )

    ciphertext = cipher.encrypt(
        pad(plaintext, BLOCK_SIZE)
    )

    return iv, ciphertext


# ------------------------------------------------------------
# Padding Oracle
#
# Returns only:
#     True  -> padding is valid
#     False -> padding is invalid
#
# The attacker cannot see the key.
# ------------------------------------------------------------
oracle_queries = 0


def padding_oracle(packet):

    global oracle_queries

    oracle_queries += 1

    # First 16 bytes = IV
    # Remaining bytes = ciphertext
    if len(packet) < 32:
        return False

    iv = packet[:BLOCK_SIZE]
    ciphertext = packet[BLOCK_SIZE:]

    if len(ciphertext) % BLOCK_SIZE != 0:
        return False

    try:

        cipher = AES.new(
            SECRET_KEY,
            AES.MODE_CBC,
            iv
        )

        plaintext = cipher.decrypt(ciphertext)

        # Check PKCS#7 padding
        unpad(plaintext, BLOCK_SIZE)

        return True

    except ValueError:

        return False


# ------------------------------------------------------------
# Padding Oracle Attack
#
# IMPORTANT:
# SECRET_KEY is NOT used here.
# ------------------------------------------------------------
def padding_oracle_attack(ciphertext, iv, oracle):

    blocks = [
        iv
    ]

    for i in range(0, len(ciphertext), BLOCK_SIZE):
        blocks.append(
            ciphertext[i:i + BLOCK_SIZE]
        )

    recovered_plaintext = bytearray()

    # Process every ciphertext block
    for block_number in range(1, len(blocks)):

        previous_block = blocks[block_number - 1]
        current_block = blocks[block_number]

        # Intermediate value:
        #
        # I = AES_DECRYPT(C)
        #
        intermediate = bytearray(BLOCK_SIZE)

        crafted_block = bytearray(previous_block)

        # Recover bytes from right to left
        for padding_value in range(1, BLOCK_SIZE + 1):

            index = BLOCK_SIZE - padding_value

            # Make already recovered bytes produce
            # the desired padding value.
            for j in range(index + 1, BLOCK_SIZE):

                crafted_block[j] = (
                    intermediate[j] ^ padding_value
                )

            found = False

            # Try all possible byte values
            for guess in range(256):

                crafted_block[index] = guess

                test_packet = (
                    bytes(crafted_block)
                    + current_block
                )

                if oracle(test_packet):

                    # Extra check for padding = 1
                    # to reduce false positives.
                    if padding_value == 1 and index > 0:

                        verification_block = bytearray(
                            crafted_block
                        )

                        verification_block[index - 1] ^= 1

                        verification_packet = (
                            bytes(verification_block)
                            + current_block
                        )

                        if not oracle(
                            verification_packet
                        ):
                            continue

                    intermediate[index] = (
                        guess ^ padding_value
                    )

                    found = True
                    break

            if not found:

                raise RuntimeError(
                    "Could not recover a plaintext byte."
                )

        # P = I XOR previous ciphertext block
        plaintext_block = bytes(
            intermediate[i] ^ previous_block[i]
            for i in range(BLOCK_SIZE)
        )

        recovered_plaintext.extend(
            plaintext_block
        )

        print(
            f"Recovered block {block_number}: "
            f"{plaintext_block}"
        )

    # Remove final PKCS#7 padding
    padding_length = recovered_plaintext[-1]

    if not (
        1 <= padding_length <= BLOCK_SIZE
    ):
        raise RuntimeError(
            "Invalid recovered padding."
        )

    if recovered_plaintext[
        -padding_length:
    ] != bytes([padding_length]) * padding_length:

        raise RuntimeError(
            "Recovered plaintext has invalid padding."
        )

    return bytes(
        recovered_plaintext[:-padding_length]
    )


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():

    plaintext = (
        b"Group01 Padding Oracle Attack Demonstration"
    )

    print("=" * 70)
    print("ASSIGNMENT 07 - PADDING ORACLE ATTACK")
    print("=" * 70)

    print("\nOriginal Plaintext:")
    print(plaintext.decode())

    # --------------------------------------------------------
    # Encryption
    # --------------------------------------------------------

    iv, ciphertext = encrypt_message(
        plaintext
    )

    print("\nIV:")
    print(iv.hex())

    print("\nCiphertext:")
    print(ciphertext.hex())

    print("\nCiphertext Length:")
    print(len(ciphertext), "bytes")

    # --------------------------------------------------------
    # Reset oracle counter
    # --------------------------------------------------------

    global oracle_queries
    oracle_queries = 0

    # --------------------------------------------------------
    # Attack
    #
    # Notice:
    # SECRET_KEY is NOT passed to this function.
    # --------------------------------------------------------

    recovered = padding_oracle_attack(
        ciphertext,
        iv,
        padding_oracle
    )

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("ATTACK RESULT")
    print("=" * 70)

    print("\nRecovered Plaintext:")
    print(recovered.decode())

    print("\nOracle Queries:")
    print(oracle_queries)

    print("\nVerification:")

    if recovered == plaintext:
        print("SUCCESS - Plaintext recovered correctly.")
    else:
        print("FAILED - Plaintext does not match.")

    print("\nKey Used During Attack:")
    print("NO - Attack function never accesses SECRET_KEY.")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
