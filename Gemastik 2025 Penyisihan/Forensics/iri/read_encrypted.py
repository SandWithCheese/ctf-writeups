import base64
from Crypto.Cipher import AES


def read_encrypted_file(filename):
    """Read the encrypted file and extract data after 0D0A bytes"""
    with open(filename, "rb") as f:
        content = f.read()

    print(f"File size: {len(content)} bytes")
    print(f"Raw content (first 100 bytes): {content[:100]}")

    # Find the position after the double 0D0A (end of headers)
    # 0D0A = \r\n = 13, 10 in decimal
    header_end = content.find(b"\r\n\r\n")
    if header_end == -1:
        print("Could not find header end (\\r\\n\\r\\n)")
        return None

    print(f"Header end found at position: {header_end}")
    print(f"Headers: {content[:header_end].decode('utf-8', errors='ignore')}")

    # Extract encrypted data after headers
    encrypted_data = content[header_end + 4 :]  # +4 to skip \r\n\r\n

    # Remove the trailing boundary
    boundary_end = encrypted_data.rfind(b"--")
    if boundary_end != -1:
        encrypted_data = encrypted_data[:boundary_end]

    print(f"Encrypted data length: {len(encrypted_data)} bytes")
    print(f"Encrypted data (hex): {encrypted_data.hex()}")

    return "74d15d28e17430ce4160507f164d27a98dec295b0164fb2f73307f4c3d947495"


def decrypt_with_aes(encrypted_data, key, iv):
    """Decrypt data using AES CBC mode"""
    try:
        # Convert hex strings to bytes
        key_bytes = bytes.fromhex(key)
        iv_bytes = bytes.fromhex(iv)

        # Create cipher
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)

        # Decrypt
        decrypted = cipher.decrypt(encrypted_data)

        # Try to remove padding
        try:
            padding_length = decrypted[-1]
            if padding_length <= 16:  # Valid padding
                decrypted = decrypted[:-padding_length]
        except:
            pass  # Keep as is if padding removal fails

        return decrypted
    except Exception as e:
        return f"Decryption error: {e}"


if __name__ == "__main__":
    # CTF key and IV
    key = "7aeaef7351e88b7a"
    iv = "b2195af3d80ec529"

    print("=== Reading Encrypted File ===")
    encrypted_data = read_encrypted_file(
        "http_objects/upload%3ffilename=last-message.txt.enc"
    )

    if encrypted_data:
        print(f"\n=== Attempting Decryption ===")
        print(f"Using key: {key}")
        print(f"Using IV: {iv}")

        # Try to decrypt
        decrypted = decrypt_with_aes(encrypted_data, key, iv)

        if isinstance(decrypted, bytes):
            print(f"\nDecrypted data (hex): {decrypted.hex()}")
            print(f"Decrypted data (raw): {decrypted}")

            # Try different encodings
            try:
                print(f"Decrypted as UTF-8: {decrypted.decode('utf-8')}")
            except:
                try:
                    print(
                        f"Decrypted as ASCII: {decrypted.decode('ascii', errors='ignore')}"
                    )
                except:
                    print("Could not decode as text")
        else:
            print(f"Decryption failed: {decrypted}")
    else:
        print("Could not read encrypted data from file")
