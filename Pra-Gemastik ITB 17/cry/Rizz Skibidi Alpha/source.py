from Crypto.Util.number import getPrime, isPrime, bytes_to_long as b2l
import random

with open('flag.txt', 'rb') as f:
    FLAG = b2l(f.read())

def generate_prime(nbits):
    p = getPrime(nbits)
    q = p 

    # iterate in range 2**500, should be impossible to bruteforce...
    r = random.randint(2, 2048)
    for _ in range(r):
        q += random.randint(2, pow(2, 500))
        
    while not isPrime(q):
        q += 1

    return p, q

p, q = generate_prime(2048)
n = p * q
e = 0x10001
ct = pow(FLAG, e, n)

assert FLAG < n

print(f'{ct = }')
print(f'{n = }')
print(f'{e = }')

