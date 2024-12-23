from Crypto.Util.number import *
import random
from secrets import bits

FLAG = b'NCW24{fake_flag}'

n = tempn = getPrime(1024)
for x in range(5):
    tempn <<= pow(5, x)
    tempn |= 5
    while not isPrime(tempn):
       tempn += 5
    n *= tempn

assert bits < 500
w, x, y, z = [random.getrandbits(bits) for _ in range(4)]
m = w**5 + x**4 + y**3 + z**2 + bytes_to_long(FLAG)

e = 65537
c = pow(m, e, n)
print(f'e =  {e}')
print(f'n =  {n}')
print(f'c =  {c}')


