import base64
from Crypto.Cipher import AES


def decrypt_flag_enc_cbc(encrypted_hex, key, iv):
    """Decrypt the flag.enc file using AES CBC mode only"""
    # Convert hex string to bytes
    encrypted_data = bytes.fromhex(encrypted_hex)

    print(f"Encrypted data length: {len(encrypted_data)} bytes")
    print(f"Encrypted data (hex): {encrypted_hex}")

    # Check if data length is multiple of 16 (AES block size)
    if len(encrypted_data) % 16 == 0:
        print("✅ Data length is multiple of 16 - suitable for CBC mode")
    else:
        print("❌ Data length is NOT multiple of 16 - CBC mode may fail")

    print(f"\n--- Using CBC Mode ---")
    try:
        # Create CBC cipher
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())

        # Decrypt
        decrypted = cipher.decrypt(encrypted_data)

        print(f"✅ CBC mode successful")
        print(f"Decrypted length: {len(decrypted)} bytes")
        print(f"Decrypted (hex): {decrypted.hex()}")

        # Try to decode as text
        try:
            text = decrypted.decode("utf-8")
            print(f"UTF-8: {text}")
        except:
            try:
                text = decrypted.decode("ascii", errors="ignore")
                print(f"ASCII: {text}")
            except:
                print("Could not decode as text")

        # Look for printable characters
        printable_count = sum(1 for b in decrypted if 32 <= b <= 126)
        print(f"Printable chars: {printable_count}/{len(decrypted)}")

        # Save decrypted data to file
        filename = "flag_decrypted_cbc.bin"
        with open(filename, "wb") as f:
            f.write(decrypted)
        print(f"Saved to: {filename}")

        return decrypted

    except Exception as e:
        print(f"❌ CBC mode failed: {e}")
        return None


if __name__ == "__main__":
    # CTF key and IV
    key = "7aeaef7351e88b7a"
    iv = "b2195af3d80ec529"

    # Encrypted flag content in hex
    encrypted_hex = "c1c866093304c73b2b3feeab7b307b7cc9ebd1e4782e426910fbae9bfd412ea0bbef86aa7c78c7d36b3ba06feb096e0f0073d47c7695a792699fdf080ff4fb49"

    print("=== Decrypting flag.enc with CBC Mode ===")
    print(f"File: flag.enc")
    print(f"Content length: {len(encrypted_hex)//2} bytes")

    # Try to decrypt with CBC only
    decrypted = decrypt_flag_enc_cbc(encrypted_hex, key, iv)

    if decrypted is not None:
        print(f"\n✅ CBC decryption successful!")
        print("Check flag_decrypted_cbc.bin for the decrypted content")
    else:
        print(f"\n❌ CBC decryption failed")
        print("The key/IV combination might be incorrect")
