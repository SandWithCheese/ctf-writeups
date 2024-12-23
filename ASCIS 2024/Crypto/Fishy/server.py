from hashlib import sha256
from random import SystemRandom
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from sage.all import *

n = 100
m = 100
q = 7
FF = GF(q)

def apply1(F, v):
    out = []
    for i in range(m):
        out.append((v.T * F[i] * v)[0, 0])
    return matrix(FF, out).T

def apply2(F, t, s):
    out = []
    for i in range(m):
        out.append((t.T * (F[i] + F[i].T) * s)[0, 0])
    return matrix(FF, out).T

def gen(v, s, F):
    output = []
    for _ in range(9):
        t = matrix(FF, [FF.random_element() for _ in range(n)]).T
        com = apply1(F, t)
        verif = apply2(F, t, s)
        a = sha256(bytes([int(i) for i in com.list() + v.list() + verif.list()])).digest()[0] % q
        output.append((com, t - a * s, verif))
    return output

def encrypt_flag(s):
    flag = open("flag.txt", "rb").read()
    key = sha256(str([int(i) for i in s.list()]).encode()).digest()
    cipher = AES.new(key, AES.MODE_CBC)
    ct = cipher.encrypt(pad(flag, 16))
    return ct, cipher.iv

rng = SystemRandom()

seed = [rng.randint(0, 255) for _ in range(64)]
gen_seed = bytes(seed)

F = []
for i in range(m):
    cur = []
    for j in range(n):
        cur.append([])
        for k in range(n):
            cur[-1].append(sha256(gen_seed).digest()[0] % q)
            gen_seed = sha256(gen_seed).digest()
    F.append(matrix(FF, n, n, cur))

s = random_matrix(FF, n, 1)	

v = apply1(F, s)
output = gen(v, s, F)

coms = [pi[0].list() for pi in output]
tass = [pi[1].list() for pi in output]
verifs = [pi[2].list() for pi in output]

ct, iv = encrypt_flag(s)

f = open("output.txt", "w")
f.write(f"{seed = }\n")
f.write(f"v = {[int(i) for i in v.list()]}\n")
f.write(f"{coms = }\n")
f.write(f"{tass = }\n")
f.write(f"{verifs = }\n")
f.write(f"{ct = }\n")
f.write(f"{iv = }")
f.close()