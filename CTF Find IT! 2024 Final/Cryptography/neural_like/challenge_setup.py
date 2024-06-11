import os
import base64
from init_vector import generate_iv
from aes import aes_encrypt
from rsa import generate_rsa_keys, cube_root
from Crypto.Util.number import bytes_to_long, long_to_bytes

padding = "XXXXXXXXXXXX"
flag = "FindITCTF{redacted}"
message = padding+flag
aes_key = os.urandom(32)
iv = generate_iv()
encrypted_message = aes_encrypt(message, aes_key, iv)

e = 3
public_keys = [generate_rsa_keys(e=e)[0] for _ in range(e)]
private_keys = [generate_rsa_keys(e=e)[1] for _ in range(e)]

message_int = bytes_to_long(aes_key)

ciphertexts = [pow(message_int, e, n) for e, n in public_keys]

encrypted_message_provided = encrypted_message
iv_provided = base64.b64encode(iv).decode('utf-8')
ciphertexts_provided = [base64.b64encode(long_to_bytes(ct)).decode('utf-8') for ct in ciphertexts]
public_keys_provided = [(e, n) for e, n in public_keys]

print("Encrypted Message:", encrypted_message_provided)
print("Initialization Vector (IV):", iv_provided)
print("Ciphertexts:", ciphertexts_provided)
print("Public Keys:", public_keys_provided)

with open('encrypted.txt', 'w') as f:
    f.write("Encrypted Message: ")
    f.write('\n')
    f.write(str(encrypted_message_provided))
    f.write('\n')
    f.write("Initialization Vector (IV): ")
    f.write('\n')
    f.write(iv_provided)
    f.write('\n')
    f.write("Ciphertexts: ")
    f.write('\n')
    f.write(str(ciphertexts_provided))
    f.write('\n')
    f.write("Public Keys: ")
    f.write('\n')
    f.write(str(public_keys_provided))
    f.write('\n')