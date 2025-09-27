import base64
import hashlib
from Crypto.Cipher import AES

key = "7aeaef7351e88b7a"
iv = "b2195af3d80ec529"


print(f"Key (hex): {key}")
print(f"Key (bytes): {key.encode()}")
print(f"IV (hex): {iv}")
print(f"IV (bytes): {iv.encode()}")
print(f"AES cipher setup completed")
print(f"Block size: {AES.block_size} bytes")
print(f"Key length: {len(key.encode())} bytes")
print(f"IV length: {len(iv.encode())} bytes")


# Example usage functions
def encrypt_data(data: str) -> str:
    """Encrypt data using AES CBC mode"""
    # Create a new cipher object for encryption
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())

    # Pad the data to block size
    padded_data = data.encode("utf-8")
    padding_length = AES.block_size - (len(padded_data) % AES.block_size)
    padded_data += bytes([padding_length] * padding_length)

    # Encrypt
    encrypted = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted).decode("utf-8")


def decrypt_data(encrypted_data: str) -> str:
    """Decrypt data using AES CBC mode"""
    try:
        # Create a new cipher object for decryption
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())

        # Decode from base64
        # encrypted_bytes = base64.b64decode(encrypted_data)

        # Decrypt
        decrypted = cipher.decrypt(encrypted_data)

        # Remove padding
        padding_length = decrypted[-1]
        decrypted = decrypted[:-padding_length]

        return decrypted
    except Exception as e:
        return f"Decryption error: {e}"


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
    print(f"Encrypted data (hex): {encrypted_data[:96]}")

    return encrypted_data[:96]


# Test the cipher
if __name__ == "__main__":
    print("=== Reading Encrypted File ===")
    encrypted_data = read_encrypted_file("http_objs/upload%3ffilename=flag.enc.i.enc")

    if encrypted_data:
        print(f"\n=== Attempting Decryption ===")
        print(f"Using key: {key}")
        print(f"Using IV: {iv}")

        # Try to decrypt
        decrypted = decrypt_data(encrypted_data)
        with open("flag.enc.i", "wb") as f:
            f.write(decrypted)

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
