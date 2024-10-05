from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt(file_path, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    with open(file_path, "rb") as file:
        original_data = file.read()
    
    padding_length = 16 - len(original_data) % 16
    padded_data = original_data + bytes([padding_length] * padding_length)
    
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    encrypted_file_path = file_path + ".enc"
    with open(encrypted_file_path, "wb") as file:
        file.write(encrypted_data)
    
    return encrypted_file_path

key = b'IFEST2024mantapp'
key = key.ljust(32, b'\x35')
iv = key[:16]
iv = bytearray(iv)
for i in range(16):
    iv[i] = iv[i] ^ 0x10
iv = bytes(iv)
encrypt('flag.png',key,iv)