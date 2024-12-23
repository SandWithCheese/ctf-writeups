from Crypto.Util.number import getPrime, bytes_to_long
import random
import os

e = 65537
p = getPrime(1024)
while (p - 1) % e == 0:
    p = getPrime(1024)

Ns = []
while len(Ns) < 4:
    q = getPrime(2048)
    N = p * q
    if (q - 1) % e != 0 and N not in Ns:
        Ns.append(N)

# flag = open("flag.txt", "rb").read()
# flag += os.urandom(3072 // 8 - 2 - len(flag))
# flag = bytes_to_long(flag)
a = Ns[0]
print(a)
print()
# cts = [pow(flag, e, N) for N in Ns]
Ns = [N + int(os.urandom(32).hex(), 16) for N in Ns]

print(Ns[0] - (Ns[0] >> 256 << 256))
os_random = Ns[0] - a
# print(hex(os_random))
# print(os_random)
avg_random = int("77" * 32, 16)
delta = avg_random - os_random
# print(delta)
random.shuffle(Ns)

# f = open("output.txt", "w")
# f.write(f"{Ns = }\n")
# f.write(f"{cts = }\n")
# f.close()
