from Crypto.Util.number import *
from Crypto.Random import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha256
import os

BLOCK_LEN = 40

flag = open("flag.txt", "rb").read()
flag1, flag2 = flag[:len(flag)//2], flag[len(flag)//2:]
flag1 = bin(bytes_to_long(flag1))[2:]
flag1 = flag1.zfill(len(flag1)+BLOCK_LEN-len(flag1)%BLOCK_LEN)
print(flag1)

p,q = getPrime(512), getPrime(512)
n = p*q
e = 11

block = [list(map(int, flag1[i:i+BLOCK_LEN])) for i in range(0, len(flag1), BLOCK_LEN)]
sums = [0 for _ in range(BLOCK_LEN)]
out = []
weight = []
key = 0

for arr in block:
    rand = [random.getrandbits(512) for _ in range(BLOCK_LEN)]
    mult = [x * y for x, y in zip(rand, arr)]
    for num in mult:
        key ^= num
    sums = [a + b for a, b in zip(sums, mult)]
    mult = [pow(m,e,n) for m in mult]
    weight.append(sum(mult))
    out.append([random.getrandbits(512) if m == 0 else m for m in mult])

key = sha256(long_to_bytes(key)).digest()
iv = os.urandom(16)
cipher = AES.new(key, AES.MODE_CBC, iv)
ct = iv + cipher.encrypt(pad(flag2, AES.block_size))

# with open("output_test.txt", "w") as f:
#     f.write(f"ct = '{ct.hex()}'\n")
#     f.write(f"out = {out}\n")
#     f.write(f"weight = {weight}\n")
#     f.write(f"sums = {sums}\n")
#     f.write(f"n = {n}\n")