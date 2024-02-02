#!/usr/bin/env python3

import random
from Crypto.Util.number import bytes_to_long, getPrime, isPrime

FLAG = b"crypto{????????????????????????????????}"

def get_complex_prime():
    D = 427
    while True:
        s = random.randint(2 ** 1020, 2 ** 1021 - 1)
        tmp = D * s ** 2 + 1
        if tmp % 4 == 0 and isPrime((tmp // 4)):
            return tmp // 4


m = bytes_to_long(FLAG)
p = get_complex_prime()
q = getPrime(2048)
n = p * q
e = 0x10001
c = pow(m, e, n)

print(f"n = {n}")
print(f"e = {e}")
print(f"c = {c}")
