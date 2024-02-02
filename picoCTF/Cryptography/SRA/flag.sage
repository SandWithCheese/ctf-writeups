from pwn import *
from Crypto.Util.number import long_to_bytes
from itertools import combinations

host, port = "saturn.picoctf.net", 57931

conn = remote(host, str(port))

c = int(conn.recvline().strip().split(b"=")[-1])
d = int(conn.recvline().strip().split(b"=")[-1])
e = 65537

kphi = d * e - 1
factors = list(factor(kphi))
kphi_factor = []
for f in factors:
    for _ in range(f[1]):
        kphi_factor.append(f[0])

for i in range(2, len(kphi_factor)):
    for combination in combinations(kphi_factor, i):
        p = product(combination) + 1
        if p.bit_length() == 128 and is_prime(p):
            kq = kphi // (p - 1)
            q_factors = list(factor(kq))
            q_factor = []
            for f in q_factors:
                for _ in range(f[1]):
                    q_factor.append(f[0])

            for j in range(2, len(q_factor)):
                for combination in combinations(q_factor, j):
                    q = product(combination) + 1
                    if q.bit_length() == 128 and is_prime(q):
                        n = p * q
                        flag = long_to_bytes(pow(c, d, n))
                        if len(flag) == 16:
                            print(flag)
                            break
                        break
                else:
                    continue
                break
    else:
        continue

conn.recvuntil(b"vainglory?")
conn.sendline(flag)

conn.interactive()
