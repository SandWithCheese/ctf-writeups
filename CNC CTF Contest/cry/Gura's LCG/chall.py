from libnum import *
from Crypto.Util.number import getPrime

class LCG:
    def __init__(self):
        self._a = getPrime(1024)
        self._b = getPrime(1024)
        self._m = getPrime(1024)
        while self._m < self._a or self._m < self._b or self._m % 4 != 3:
            self._m = getPrime(1024)

        self._seed = getPrime(1024)
        for i in range(257):
            self.next()
    
    def next(self):
        self._seed = (self._seed * self._a + self._b) % self._m
        return self._seed
            
vals = []
lcg = LCG()
for i in range(12):
    lcg.next()
    vals.append(str(lcg.next()) + "\n")
    
flag = open("flag.txt", "rb").read().strip()

with open("../bin/out.txt", "w+") as f:
    f.write(str(lcg._m) + "\n")
    f.writelines(vals)
    f.write(str(s2n(flag) ^ lcg.next()))