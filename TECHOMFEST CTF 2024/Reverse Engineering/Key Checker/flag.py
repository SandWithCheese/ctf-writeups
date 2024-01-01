a = "5a15715955270e75"
b = "370854130a"
c = "39727e"
d = "4f721d1555"
e = "5c552d5857311246"

xor = ""
for i in range(len(a), 0, -2):
    xor += a[i - 2 : i]

for i in range(len(b), 0, -2):
    xor += b[i - 2 : i]

for i in range(len(c), 0, -2):
    xor += c[i - 2 : i]

for i in range(len(d), 0, -2):
    xor += d[i - 2 : i]

for i in range(len(e), 0, -2):
    xor += e[i - 2 : i]

flag = [
    int(xor[:2], 16),
    int(xor[2:4], 16),
    int(xor[4:6], 16),
    int(xor[6:8], 16),
    int(xor[8:10], 16),
    int(xor[10:12], 16),
    int(xor[12:14], 16),
]
flag = list(map(chr, flag))

idx = 0
for i in range(14, len(xor), 2):
    flag.append(chr(ord(flag[idx % len(flag)]) ^ int(xor[i : i + 2], 16)))
    idx += 1

tcf = "TCF2024"

key = []
for i in range(len(tcf)):
    key.append(chr(ord(flag[i]) ^ ord(tcf[i])))

idx = 0
for i in range(0, len(xor), 2):
    block = int(xor[i : i + 2], 16)
    print(chr(block ^ ord(key[idx % len(key)])), end="")
    idx += 1
