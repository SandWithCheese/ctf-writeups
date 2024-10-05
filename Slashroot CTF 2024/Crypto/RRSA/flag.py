from pwn import *
from Crypto.Util.number import isPrime, long_to_bytes
from math import gcd
from functools import reduce


class RandomSequenceGenerator:
    def __init__(self, a, b, c, s):
        self.a = a
        self.b = b
        self.c = c
        self._current_value = s

    def next(self):
        tmp = self._current_value * self.a
        adj = tmp + self.b
        self._current_value = divmod(adj, self.c)[1]
        return self._current_value


host, port = "157.230.251.184", "10012"

conn = remote(host, port)

conn.recvline()
conn.recvline()
conn.recvline()
conn.recvline()
conn.recvline()
conn.recvline()
conn.recvline()
conn.recvline()
conn.recvline()
conn.recvline()
conn.recvline()
conn.recvline()
conn.recvline()

n = int(conn.recvline().strip().decode().split(" : ")[1], 16)

conn.sendlineafter(b"> ", b"2")
hint = eval(conn.recvline().strip().decode().split(" : ")[1])

shift = 10
cands = []
for cand in hint:
    cands.append(cand >> pow(2, shift))
    if isPrime(cand >> pow(2, shift)):
        print("Found prime!")
        exit()


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)


def modinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n


def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0] * multiplier) % modulus
    return modulus, multiplier, increment


def crack_unknown_multiplier(states, modulus):
    multiplier = (
        (states[2] - states[1]) * modinv(states[1] - states[0], modulus) % modulus
    )
    return crack_unknown_increment(states, modulus, multiplier)


def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2 * t0 - t1 * t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(reduce(gcd, zeroes))
    return crack_unknown_multiplier(states, modulus)


c, a, b = crack_unknown_modulus(cands[:7])

rng = RandomSequenceGenerator(a, b, c, cands[0])

primes = []
tmp_n = n
i = 1
while tmp_n != 1:
    cand = rng.next()
    if isPrime(cand):
        primes.append(cand)
        tmp_n //= cand
    i += 1

e = 65537

conn.sendlineafter(b"> ", b"1")
dec_flag = int(conn.recvline().strip().decode().split(" : ")[1], 16)

phi = 1
for prime in primes:
    phi *= prime - 1

d = pow(e, -1, phi)

flag = pow(dec_flag, d, n)
flag = long_to_bytes(flag)
print(flag)

conn.interactive()
