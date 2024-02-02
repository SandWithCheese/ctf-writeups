#! usr/bin/env Python3
import random
import math
import sympy
from sympy import mod_inverse

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, num // 2 + 1):
        if num % i == 0:
            return False
    return True


def generate_prime(min_val, max_val):
    prime = random.randint(min_val, max_val)
    while not is_prime(prime):
        prime = random.randint(min_val, max_val)
    return prime


p, q = generate_prime(1000000000000000000000000, 10000000000000000000000000), generate_prime(1000000000000000000000000, 10000000000000000000000000)
while p == q:
    q = generate_prime(1000000000000000000000000, 10000000000000000000000000)

n = p*q
phi = (p-1)*(q-1)

e = random.randint(3, phi-1)
while math.gcd(e, phi) != 1:
    e = random.randint(3, phi-1)

d = mod_inverse(e, phi)

print("Public Key: [",e, n,"]")
print("Private Key: [",d, n,"]")
print("N is: ",n)
print("Phi is: ",phi)
print("P is: ",p)
print("Q is: ",q)

plaintext = "ARA{REDACTED}"
encodedtext = [ord(ch) for ch in plaintext]

# (txt ^ e) mod n = cph
ciphertext = [pow(ch, e, n) for ch in encodedtext]
print(ciphertext)


# (cph ^ d) mod n = txt
encodedtext = [pow(ch, d, n) for ch in ciphertext]
plaintext = "".join(chr(ch) for ch in encodedtext)

print(plaintext)
