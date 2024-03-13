from Crypto.Util.number import getStrongPrime
from fractions import gcd
from secret import flag

def get_key(e=65537, bit_length=2048):
    while True:
        p = getStrongPrime(bit_length, e=e)
        q = getStrongPrime(bit_length, e=e)
        if gcd(e, (p - 1) * (q - 1)) == 1:
            return e, p * q

def encrypt(e, n, m):
    return [((ord(c) ** e) % n) for c in m]

e, n = get_key()

print("Generated key:")
print(e)
print(n)

print("Encrypted flag:")
print(encrypt(e, n, flag))
