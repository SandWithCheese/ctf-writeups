from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def decrypt(file_path, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    with open(file_path, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    padding_length = decrypted_data[-1]
    original_data = decrypted_data[:-padding_length]

    decrypted_file_path = file_path[:-4]
    with open(decrypted_file_path, "wb") as file:
        file.write(original_data)

    return decrypted_file_path


key = b"IFEST2024mantapp5555555555555555"
iv = b'YVUCD" "$}q~dq``'


decrypt("flag.png.enc", key, iv)
