from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import unpad
import zlib

encrypted_hex = "c1c866093304c73b2b3feeab7b307b7cc9ebd1e4782e426910fbae9bfd412ea0bbef86aa7c78c7d36b3ba06feb096e0f0073d47c7695a792699fdf080ff4fb49"
ciphertext = bytes.fromhex(encrypted_hex)
key = b"SuperSecretKey!!"
iv = b"12345678"

cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
decrypted_padded = cipher.decrypt(ciphertext)
try:
    flag_bytes = unpad(decrypted_padded, Blowfish.block_size)
except ValueError:
    # If unpad fails, just use the raw bytes
    flag_bytes = decrypted_padded

print(flag_bytes)
