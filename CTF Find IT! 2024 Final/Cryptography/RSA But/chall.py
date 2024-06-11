from Crypto.Util.number import *

def prime():
    a = getStrongPrime(4096)
    b = getStrongPrime(4096)
    c = getStrongPrime(4096)
    return a, b, c

flag = open('secret','rb').read()

c1, c2 = bytes_to_long(flag[:len(flag)//2]), bytes_to_long(flag[len(flag)//2:])

p1, q1, q2 = prime()
p2 = p1
e = 0x10001
n1 = p1 * q1
n2 = p2 * q2

enc1 = pow(c1, e, n1)
enc2 = pow(c2, e, n2)

pq = p1 + q1

print(f"""n1 = {n1}
n2 = {n2}
enc1 = {enc1}
enc2 = {enc2}
e = {e}
pq = {pq}""")