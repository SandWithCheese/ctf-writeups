from Crypto.Util.number import long_to_bytes
from libnum import n2s

with open("broken_rsa_34db5007b0788a5cd306f3bd47e9ca71.txt", "r") as f:
    n = int(f.readline().strip().split()[-1])
    e = int(f.readline().strip().split()[-1])
    c = int(f.readline().strip().split()[-1])

R.<x> = Zmod(n)[]
f = x^2 - c

r8 = [i[0] for i in f.roots()]
r4 = []
print("sat")
for i in r8:
    f = x^2 - i
    r4 += [i[0] for i in f.roots()]

r2 = []
print("sat")
for i in r4:
    f = x^2 - i
    r2 += [i[0] for i in f.roots()]

r = []
print("sat")
for i in r2:
    f = x^2 - i
    r += [i[0] for i in f.roots()]

print("sat")
for m in r:
    try:
        print(n2s(int(m)))
    except:
        print("Fail")