# from pwn import *

# host, port = "27.112.79.222", "8012"

# nec_pair = []

# for i in range(200):
#     conn = remote(host, port)

#     n = int(conn.recvline().decode().split("=")[1].strip())
#     e = int(conn.recvline().decode().split("=")[1].strip())
#     c = int(conn.recvline().decode().split("=")[1].strip())

#     nec_pair.append((n, e, c))

#     conn.close()

# with open("nec_pairs.txt", "w") as f:
#     f.write(f"nec_pair={nec_pair}")

# conn.interactive()

from itertools import combinations
from functools import reduce
from gmpy2 import iroot
from Crypto.Util.number import long_to_bytes


def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


with open("nec_pairs.txt", "r") as f:
    nec_pair = eval(f.read().split("=")[1])

# Group nec_pairs based on its e value

grouped_nec_pair = {}

for n, e, c in nec_pair:
    if e not in grouped_nec_pair:
        grouped_nec_pair[e] = []

    grouped_nec_pair[e].append((n, e, c))

for e, nec_pairs in grouped_nec_pair.items():
    print(f"e = {e}")
    for combi in combinations(nec_pairs, 3):
        n = [n for n, _, _ in combi]
        c = [c for _, _, c in combi]

        m = chinese_remainder(n, c)
        m = iroot(m, e)[0]

        try:
            print(long_to_bytes(m).decode())
        except:
            pass


# for combi in combinations(nec_pair, 3):
#     print(list(combi))
#     break
