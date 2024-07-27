from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

with open("flag.png", "rb") as f:
    flag = f.read()

key = os.urandom(1) * 16 
iv = os.urandom(16)

cipher = AES.new(key, AES.MODE_CBC, iv)

ciphertext = cipher.encrypt(pad(flag, AES.block_size))

with open("flag.enc", "wb") as f:
    f.write(iv + ciphertext)

