from Crypto.Util.number import *
from sympy import nextprime

flag = open("flag.txt").read().strip().encode()
m = nextprime(bytes_to_long(flag))

p = getPrime(512)
q = getPrime(512)
n = p * q
e = 3

M = Matrix([[m, p], [q, m+3]])
C = M ^ e

print(f"C = {C.list()}")
print(f"e = {e}")
print(f"n = {n}")