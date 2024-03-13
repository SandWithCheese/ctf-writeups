import pwn
import sympy
from itertools import combinations

host, port = "saturn.picoctf.net", 54989

n_len = 128 * 2

conn = pwn.remote(host, port)

e = 65537
c = int(conn.recvline().decode().strip().split()[2])
d = int(conn.recvline().decode().strip().split()[2])

primes = sympy.primefactors(e * d - 1)
print(primes)

possible_phi = []
for i in range(2, len(primes)):
    print(i)
    combs = list(combinations(primes, i))
    for comb in combs:
        total = 1
        for e in comb:
            total *= e
        bin_tot = bin(total)[2:]
        if n_len - 10 <= len(bin_tot) <= n_len + 10:
            possible_phi.append(total)

print(possible_phi)

conn.interactive()
