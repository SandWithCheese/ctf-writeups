from Crypto.Cipher import AES
import os

KEY = os.urandom(16)
iv = os.urandom(16)

ct = b"A" * 32

cipher = AES.new(KEY, AES.MODE_CFB, iv=iv, segment_size=16)
pt = cipher.decrypt(ct)

# will repeat every 16 bits (2 bytes)
print(pt)  # b"AbAbAbAbAbAbAbAbAbAbAbAbAbAbAbAb"
