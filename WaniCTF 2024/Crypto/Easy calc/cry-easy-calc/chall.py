import os
import random
from hashlib import md5

from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes, getPrime

FLAG = os.getenvb(b"FLAG", b"FAKE{THIS_IS_NOT_THE_FLAG!!!!!!}")


def encrypt(m: bytes, key: int) -> bytes:
    iv = os.urandom(16)
    key = long_to_bytes(key)
    key = md5(key).digest()
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return iv + cipher.encrypt(m)


def f(s, p):
    u = 0
    for i in range(p):
        u += p - i
        u *= s
        u %= p

    return u


p = getPrime(1024)
s = random.randint(1, p - 1)

A = f(s, p)
ciphertext = encrypt(FLAG, s).hex()


print(f"{p = }")
print(f"{A = }")
print(f"{ciphertext = }")
