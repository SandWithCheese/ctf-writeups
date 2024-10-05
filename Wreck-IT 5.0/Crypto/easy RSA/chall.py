from Crypto.Util.number import isPrime, bytes_to_long
import random

FLAG = b"WRECKIT50{REDACTED}"

def getPrime():
	while True:
		a, b, c = random.getrandbits(512), random.getrandbits(512),  random.getrandbits(512)
		p = (a * (3**2048)) + (b * (3**1024)) + c
		if isPrime(p): return p

p = getPrime()
q = getPrime()

n = p * q
e = 0x10001
m = bytes_to_long(FLAG)
c = pow(m, e, n)

tulis = open('hasil.txt','w')
tulis.write(f"n = {n}\n")
tulis.write(f"e = {e}\n")
tulis.write(f"c = {c}\n")
