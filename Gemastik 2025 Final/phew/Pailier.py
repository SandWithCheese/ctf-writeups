from Crypto.Util.number import *
from math import lcm
import random

class pailier:
    def __init__(self):
        self.primes = [getPrime(200) for _ in range(2)]
        self.n = 1
        self.phi = 1
        self.mul = 1
        for i in range(2):
            self.n  *= self.primes[i]
            self.phi *= (self.primes[i] - 1)  
        self.n2 = self.n * self.n
        self.g = [pow(random.randrange(1, self.n2), self.primes[i], self.n2) for i in range(2)]
        for x in self.g:
            self.mul = (self.mul * x) % self.n2
        self.miu = inverse(self.L(pow(self.mul, self.phi, self.n2)), self.n)
        self.alpha = [None, None]
        for idx in range(2):
            while True:
                a = random.randrange(2, self.n - 1)
                if GCD(a, self.n) == 1:
                    self.alpha[idx] = a
                    break
        self.beta  = [random.randrange(0, self.n), random.randrange(0, self.n)]

    def L(self, val):
        return (val - 1) // self.n

    def pubkey(self):
        return (self.n, self.g)

    def encrypt(self, msg: int) -> int:
        r  = random.randrange(0, self.n - 1)
        gb = self.g[random.randrange(0, 2)]
        gm = pow(gb, msg, self.n2)
        rn = pow(r, self.n, self.n2)
        return (gm * rn) % self.n2

    def decrypt(self, ct: int) -> int:
        raw = self.L(pow(ct, self.phi, self.n2)) % self.n
        raw = (raw * self.miu) % self.n
        t = pow(ct % self.n, (self.n - 1) // 2, self.n) if (self.n % 2 == 1) else 0
        idx = 0 if t == 1 else 1
        return (self.alpha[idx] * raw + self.beta[idx]) % self.n

