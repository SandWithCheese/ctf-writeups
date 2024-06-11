from Crypto.Util.number import getPrime, bytes_to_long as b2l
from random import randint

with open("flag.txt", "rb") as f:
    FLAG = b2l(f.read())

nbits = 1024

p = getPrime(nbits)
q = getPrime(nbits)
n = p * q
e = 0x10001
ct = pow(FLAG, e, n)

bin_p = format(p, "b")
print(bin_p)
# print(len(bin_p))
bin_p = [int(bin_p[i : i + 32], 2) for i in range(0, len(bin_p), 32)]

temp = ""
for binary in bin_p:
    temp += format(binary, "032b")

print(temp)
# print(bin_p == temp)

rand = [[randint(2, nbits) for _ in range(nbits // 32)] for _ in range(nbits // 32)]

leak = []
for i in range(len(rand)):
    val = 0
    for j in range(len(rand[0])):
        val += bin_p[j] * rand[i][j]
    leak.append(val)

print(f"{ct = }")
print(f"{n = }")
print(f"{e = }")
print(f"{rand = }")
print(f"{leak = }")
