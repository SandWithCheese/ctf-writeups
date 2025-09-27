import argparse
from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad

# Blowfish key (between 4 and 56 bytes). We'll use 16 bytes here.
key = b'SuperSecretKey!!'  # change to your own

# Blowfish IV must be exactly 8 bytes (block size)
iv = b'12345678'

BLOCK_SIZE = Blowfish.block_size  # 8

def encrypt_file(input_file, output_file):
    """Encrypt a file using Blowfish-CBC."""
    with open(input_file, 'rb') as f:
        plaintext = f.read()

    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    padded_plaintext = pad(plaintext, BLOCK_SIZE)
    ciphertext = cipher.encrypt(padded_plaintext)

    with open(output_file, 'wb') as f:
        f.write(ciphertext)

    print(f'[+] File encrypted successfully → {output_file}')

def decrypt_file(input_file, output_file):
    """Decrypt a file using Blowfish-CBC."""
    with open(input_file, 'rb') as f:
        ciphertext = f.read()

    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(ciphertext)
    plaintext = unpad(decrypted_data, BLOCK_SIZE)

    with open(output_file, 'wb') as f:
        f.write(plaintext)

    print(f'[+] File decrypted successfully → {output_file}')

def main():
    parser = argparse.ArgumentParser(description="Encrypt or decrypt a file using Blowfish-CBC.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--encrypt', action='store_true', help="Encrypt the file.")
    group.add_argument('--decrypt', action='store_true', help="Decrypt the file.")
    parser.add_argument('--input', type=str, required=True, help="Input file path.")
    parser.add_argument('--output', type=str, required=True, help="Output file path.")

    args = parser.parse_args()

    if args.encrypt:
        encrypt_file(args.input, args.output)
    elif args.decrypt:
        decrypt_file(args.input, args.output)

if __name__ == "__main__":
    main()
