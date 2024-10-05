from Crypto.Util.number import long_to_bytes
from math import gcd

with open("chall2_mem.txt", "r") as f:
    n = eval(f.readline().split(" = ")[1])
    e = eval(f.readline().split(" = ")[1])
    c = eval(f.readline().split(" = ")[1])

for i in range(15, 0, -1):
    n1 = n[i]
    p1 = gcd(n1, n[i - 1])
    q1 = n1 // p1

    phi1 = (p1 - 1) * (q1 - 1)
    d1 = pow(e, -1, phi1)
    c = pow(c, d1, n1)

n0 = n[0]
p0 = gcd(n0, n1)
q0 = n0 // p0

phi0 = (p0 - 1) * (q0 - 1)
d0 = pow(e, -1, phi0)
m = pow(c, d0, n0)

print(long_to_bytes(m).decode())
