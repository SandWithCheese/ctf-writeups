import os, functools
from Crypto.Util.number import *
from flagg import flag

p = []
e = 2

for i in range(10):
    p.append(getPrime(1024))


m = bytes_to_long(os.urandom(256) + flag)
n = functools.reduce((lambda x, y: x * y), p)
c = pow(m,e,n)

with open("chall.txt", "w") as f:
    f.write("p:\n")
    for i in p:
        f.write(str(i) + "\n")
    f.write("\nc:\n")
    f.write(str(c))


