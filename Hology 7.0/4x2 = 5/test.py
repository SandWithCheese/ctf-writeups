import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii


# Fungsi untuk membuat hash SHA-256
def sha256_hash(password):
    return hashlib.sha256(password.encode()).digest()


# Fungsi untuk mengenkripsi menggunakan AES
def aes_encrypt(key, data):
    # Membuat cipher AES
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv + ct_bytes  # Mengembalikan IV + ciphertext


# Kunci dan kata sandi
key_hex = "4b6e25b2a0db4eef250e746f391c97f0"
key = binascii.unhexlify(key_hex)  # Mengubah kunci dari hex ke bytes
password = "HealthKathon2024"

# Langkah 1: Hash dengan SHA-256
hashed_password = sha256_hash(password)

# Langkah 2: Enkripsi dengan AES
encrypted_hash = aes_encrypt(key, hashed_password)

# Mencetak hasil dalam format hexadecimal
target_hash_hex = binascii.hexlify(encrypted_hash).decode()
print(f"Target Hash: {target_hash_hex}")

import itertools
import string


# Fungsi untuk mencocokkan dengan hash target
def matches_target_hash(password, target_hash_hex):
    hashed_password = sha256_hash(password)
    encrypted_hash = aes_encrypt(key, hashed_password)
    return binascii.hexlify(encrypted_hash).decode() == target_hash_hex


# Daftar karakter yang ingin dicoba
characters = string.ascii_letters + string.digits + string.punctuation

# Mencari kata sandi yang sesuai
for length in range(1, 6):  # Uji panjang kata sandi dari 1 hingga 5
    for password in itertools.product(characters, repeat=length):
        password = "".join(password)
        if matches_target_hash(password, target_hash_hex):
            print(f"Found password: BPJS{{{password}}}")
            break
