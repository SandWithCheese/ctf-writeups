import random
from hashlib import sha256

from Crypto.Cipher import AES
from Crypto.Util.number import getPrime, long_to_bytes
from Crypto.Util.Padding import pad
from function import *

# from secret import FLAG, iiv, x, y, z
FLAG = b"FindIT{REDACTED}"

iiv = 81
x = 3
y = 4
z = 16

with open("test.txt", "w") as file:
    file.write("")


def write(text):
    with open("test.txt", "a") as file:
        file.write(str(text) + "\n")


p = getPrime(64)
p1 = convert(f"0x{p:x}", x)
write(f"p = {p1}")

g = random.randint(1, p - 1)
g1 = convert(f"0x{g:x}", y)
write(f"g = {g1}")

a = random.randint(1, p - 1)
b = random.randint(1, p - 1)

A, B = pow(g, a, p), pow(g, b, p)

write(f"A = {bin(A)}")
write(f"B = {oct(B)}")

C = pow(A, b, p)
assert C == pow(B, a, p)

assert iiv == pow(x, y)
iiv = modify_digit(iiv, rules)

hash = sha256()
hash.update(long_to_bytes(C))

key = hash.digest()[:16]
iv = iiv.to_bytes(z, byteorder="little")
cipher = AES.new(key, AES.MODE_CBC, iv)

encrypted = cipher.encrypt(pad(FLAG, z**2))
f = open("c", "wb")
f.write(encrypted)
f.close()
write(f"c = {encrypted}")
