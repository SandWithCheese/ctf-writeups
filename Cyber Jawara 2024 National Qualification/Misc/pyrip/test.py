from Crypto.Cipher import AES
from pwn import xor

key = b"\x01" * 16
iv = b"\x01" * 16
cipher1 = AES.new(key, AES.MODE_CBC, iv=iv)
print(cipher1.encrypt(b"\x00" * 16))

cipher2 = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128)
print(cipher2.encrypt(b"\x00" * 16))
