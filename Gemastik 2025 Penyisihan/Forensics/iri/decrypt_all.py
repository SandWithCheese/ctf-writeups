#!/usr/bin/env python3
import os
import urllib.parse
from Crypto.Cipher import AES

# --- CONFIGURATION ---
# AES key and IV are the same for all files.
KEY = "7aeaef7351e88b7a".encode()
IV = "b2195af3d80ec529".encode()

# Directories for input and output.
INPUT_DIR = "http_objs"
OUTPUT_DIR = "decrypted_files"


def extract_payload(file_path: str) -> bytes | None:
    """
    Reads an encrypted file dump and extracts the raw encrypted data payload.
    The payload is located after the HTTP headers (after \\r\\n\\r\\n).
    """
    try:
        with open(file_path, "rb") as f:
            content = f.read()
    except IOError as e:
        print(f"  [!] Error reading file {file_path}: {e}")
        return None

    # Find the end of the HTTP headers
    header_end = content.find(b"\r\n\r\n")
    if header_end == -1:
        print(f"  [!] Could not find HTTP header end in {os.path.basename(file_path)}")
        return None

    # The encrypted data starts 4 bytes after the header end
    encrypted_data = content[header_end + 4 :]

    # Clean up the multipart form data boundary at the end of the file
    # This is often "--" followed by a boundary string and more "--".
    # We can simplify by finding the last occurrence of the boundary start.
    boundary_marker = b"\r\n--"
    boundary_pos = encrypted_data.rfind(boundary_marker)
    if boundary_pos != -1:
        encrypted_data = encrypted_data[:boundary_pos]

    return encrypted_data


def decrypt_data(encrypted_data: bytes) -> bytes | None:
    """
    Decrypts data using AES CBC mode and removes PKCS#7 padding.
    """
    try:
        cipher = AES.new(KEY, AES.MODE_CBC, IV)
        decrypted_padded = cipher.decrypt(encrypted_data)

        # Remove PKCS#7 padding
        padding_length = decrypted_padded[-1]
        if padding_length > AES.block_size:
            # This indicates bad padding, likely a decryption error.
            return None
        decrypted = decrypted_padded[:-padding_length]
        return decrypted
    except Exception as e:
        # Catches value errors from bad padding or other crypto issues.
        print(f"  [!] Decryption failed: {e}")
        return None


def main():
    """
    Main function to find, decrypt, and save all encrypted files.
    """
    if not os.path.isdir(INPUT_DIR):
        print(f"Error: Input directory '{INPUT_DIR}' not found.")
        print(
            "Please make sure the http_objs directory is in the same folder as this script."
        )
        return

    # Create the output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"[*] Decrypted files will be saved in '{OUTPUT_DIR}'\n")

    # Process each file in the input directory
    for filename in sorted(os.listdir(INPUT_DIR)):
        if not filename.endswith(".enc"):
            continue

        print(f"[*] Processing: {filename}")
        input_path = os.path.join(INPUT_DIR, filename)

        # 1. Extract the encrypted payload from the HTTP dump
        payload = extract_payload(input_path)
        if not payload:
            continue

        # 2. Decrypt the payload
        decrypted_content = decrypt_data(payload)
        if not decrypted_content:
            continue

        # 3. Determine the correct original filename
        decoded_url = urllib.parse.unquote(filename)

        # We need to handle two cases: `upload?filename=...` and direct paths like `/%2f(1)`
        if "upload?filename=" in decoded_url:
            # This extracts 'script.py.enc' from 'upload?filename=script.py.enc'
            original_filename = decoded_url.split("filename=")[-1]
        else:
            # This handles files like '%2f(27).enc' which becomes '/(27).enc'
            original_filename = decoded_url

        # Remove the final .enc extension and clean up path characters
        output_filename = original_filename.replace(".enc", "").replace("/", "_")

        # 4. Save the decrypted file
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        try:
            with open(output_path, "wb") as f:
                f.write(decrypted_content)
            print(f"  [+] Success: Saved to {output_path}")
        except IOError as e:
            print(f"  [!] Error saving file {output_path}: {e}")

    print("\n[*] All files processed.")


if __name__ == "__main__":
    main()
