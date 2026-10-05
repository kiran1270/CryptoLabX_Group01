from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 16

# ============================================================
# ORACLE SETUP
# ============================================================
# IMPORTANT:
# The attacker will NOT receive this key.
# It is kept internally by the encryption/oracle.
# ============================================================

SECRET_KEY = get_random_bytes(16)

SECRET_MESSAGE = (
    b"Group01 ID2024UCP1270 Padding Oracle Attack Demonstration"
)


def pkcs7_pad(data):
    padding_length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([padding_length]) * padding_length


def encrypt_message(plaintext):
    """
    Encrypt plaintext using AES-CBC.
    Returns IV + ciphertext.
    """

    iv = get_random_bytes(BLOCK_SIZE)

    cipher = AES.new(
        SECRET_KEY,
        AES.MODE_CBC,
        iv
    )

    padded = pkcs7_pad(plaintext)

    ciphertext = cipher.encrypt(padded)

    return iv + ciphertext


# ============================================================
# PADDING ORACLE
# ============================================================

oracle_queries = 0


def padding_oracle(ciphertext):
    """
    Returns True if the decrypted ciphertext has valid PKCS#7
    padding, otherwise False.

    The AES key is hidden inside this function.
    The attacker only gets True/False.
    """

    global oracle_queries
    oracle_queries += 1

    if len(ciphertext) < 32:
        return False

    try:
        iv = ciphertext[:BLOCK_SIZE]
        encrypted_data = ciphertext[BLOCK_SIZE:]

        cipher = AES.new(
            SECRET_KEY,
            AES.MODE_CBC,
            iv
        )

        plaintext = cipher.decrypt(encrypted_data)

        # Check PKCS#7 padding
        padding_length = plaintext[-1]

        if padding_length < 1 or padding_length > BLOCK_SIZE:
            return False

        padding = plaintext[-padding_length:]

        if padding != bytes([padding_length]) * padding_length:
            return False

        return True

    except Exception:
        return False


# ============================================================
# PADDING ORACLE ATTACK
# ============================================================

def recover_block(previous_block, target_block):
    """
    Recover one plaintext block without knowing the AES key.

    previous_block = C(i-1)
    target_block   = C(i)

    CBC decryption:

        P(i) = D(C(i)) XOR C(i-1)

    We modify C(i-1) and use the padding oracle
    to recover P(i) from right to left.
    """

    intermediate = [0] * BLOCK_SIZE
    recovered = [0] * BLOCK_SIZE

    # Work from last byte to first byte
    for position in range(BLOCK_SIZE - 1, -1, -1):

        padding_value = BLOCK_SIZE - position

        # Create modified previous block
        modified_previous = bytearray(previous_block)

        # Force already recovered bytes to have desired padding
        for j in range(position + 1, BLOCK_SIZE):
            modified_previous[j] = (
                previous_block[j]
                ^ intermediate[j]
                ^ padding_value
            )

        found = False

        # Try all possible byte values
        for guess in range(256):

            modified_previous[position] = (
                previous_block[position]
                ^ guess
                ^ padding_value
            )

            test_ciphertext = (
                bytes(modified_previous) + target_block
            )

            if padding_oracle(test_ciphertext):

                # Extra verification for the last byte
                # to avoid false positives caused by existing padding.
                if position == BLOCK_SIZE - 1:

                    verification = bytearray(modified_previous)

                    verification[position - 1] ^= 1

                    if not padding_oracle(
                        bytes(verification) + target_block
                    ):
                        continue

                intermediate[position] = guess

                recovered[position] = (
                    guess ^ previous_block[position]
                )

                found = True
                break

        if not found:
            raise RuntimeError(
                f"Could not recover byte at position {position}"
            )

    return bytes(recovered)


def remove_pkcs7_padding(data):
    """
    Remove PKCS#7 padding after the complete plaintext
    has been recovered.
    """

    padding_length = data[-1]

    if padding_length < 1 or padding_length > BLOCK_SIZE:
        raise ValueError("Invalid PKCS#7 padding")

    if data[-padding_length:] != bytes([padding_length]) * padding_length:
        raise ValueError("Invalid PKCS#7 padding")

    return data[:-padding_length]


def padding_oracle_attack(full_ciphertext):
    """
    Recover complete plaintext.

    The attacker knows:
        IV
        ciphertext
        padding oracle

    The attacker does NOT know:
        AES key
    """

    iv = full_ciphertext[:BLOCK_SIZE]
    ciphertext = full_ciphertext[BLOCK_SIZE:]

    blocks = [
        ciphertext[i:i + BLOCK_SIZE]
        for i in range(0, len(ciphertext), BLOCK_SIZE)
    ]

    recovered_plaintext = b""

    previous_block = iv

    for block_number, target_block in enumerate(blocks, start=1):

        print(
            f"Recovering plaintext block {block_number}/{len(blocks)}..."
        )

        plaintext_block = recover_block(
            previous_block,
            target_block
        )

        recovered_plaintext += plaintext_block

        previous_block = target_block

    return remove_pkcs7_padding(recovered_plaintext)


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("=" * 70)
    print("ASSIGNMENT 07 - PADDING ORACLE ATTACK")
    print("=" * 70)

    print("\nGroup No. : 01")
    print("Student ID: 2024UCP1270")

    # --------------------------------------------------------
    # Encrypt the secret message.
    #
    # In a real attack, the attacker would simply receive
    # this IV + ciphertext from the vulnerable application.
    # --------------------------------------------------------

    encrypted_message = encrypt_message(SECRET_MESSAGE)

    iv = encrypted_message[:BLOCK_SIZE]
    ciphertext = encrypted_message[BLOCK_SIZE:]

    print("\nIV:")
    print(iv.hex())

    print("\nCiphertext:")
    print(ciphertext.hex())

    print("\nCiphertext length:", len(ciphertext), "bytes")

    # Reset oracle query counter before attack
    global oracle_queries
    oracle_queries = 0

    print("\nStarting Padding Oracle Attack...")
    print("AES key is NOT provided to the attacker.")

    recovered = padding_oracle_attack(encrypted_message)

    print("\n" + "=" * 70)
    print("ATTACK COMPLETED")
    print("=" * 70)

    print("\nRecovered plaintext:")
    print(recovered.decode())

    print("\nOracle queries required:")
    print(oracle_queries)

    print("\nVerification:")
    print("Recovered plaintext matches original:",
          recovered == SECRET_MESSAGE)

    print("\nThe AES key was never used by the attack function.")


if __name__ == "__main__":
    main()
