from Cryptodome.Util.number import getPrime, inverse, bytes_to_long
from math import gcd
import re
import random
import string
# from flag import flag
flag = "FindITCTF{REDACTED}"

while True:
    p = getPrime(1024)
    q = getPrime(1024)

    n = p * q
    e = 3
    phi = (p-1)*(q-1)

    if gcd(phi, e) == 1:
        d = inverse(e, phi)
        break


def pad():
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=12))

if __name__ == "__main__":
    evolutions = ['alpha', 'sigma', 'ligma', 'omega', 'skibi', 'rizlr']
    e1 = random.choice(evolutions)
    while True:
        e2 = random.choice(evolutions)
        if e2 != e1:
            break

    flag1 = re.sub("beta", e1, flag) + pad()
    flag2 = re.sub("beta", e2, flag) + pad()

    print(flag1)
    print(flag2)

    fl1 = bytes_to_long(flag1.encode())
    fl2 = bytes_to_long(flag2.encode())

    ct1 = pow(fl1, e, n)
    ct2 = pow(fl2, e, n)

    print(f"n = {n}")
    print(f"e = {e}")
    print(f"ct1 = {ct1}")
    print(f"ct2 = {ct2}")

