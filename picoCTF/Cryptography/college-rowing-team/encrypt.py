#!/usr/bin/env python3

import random
from Crypto.Util.number import getPrime, bytes_to_long

with open('flag.txt', 'rb') as f:
    flag = f.read()

msgs = [
    b'I just cannot wait for rowing practice today!',
    b'I hope we win that big rowing match next week!',
    b'Rowing is such a fun sport!'
        ]

msgs.append(flag)
msgs *= 3
random.shuffle(msgs)

for msg in msgs:
    p = getPrime(1024)
    q = getPrime(1024)
    n = p * q
    e = 3
    m = bytes_to_long(msg)
    c = pow(m, e, n)
    with open('encrypted-messages.txt', 'a') as f:
        f.write(f'n: {n}\n')
        f.write(f'e: {e}\n')
        f.write(f'c: {c}\n\n')