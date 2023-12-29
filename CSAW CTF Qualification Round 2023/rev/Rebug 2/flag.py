hexstr = "6e3762597041674244777343"

flag = ""

for i in range(4, len(hexstr), 2):
    block = hexstr[i : i + 2]
    binstr = ""

    for j in range(8):
        tmp = int(block, 16) << (j & 31) >> 7 & 1
        binstr += str(tmp)

    a, b = binstr[:4], binstr[4:]
    xor = int(a, 2) ^ int(b, 2)
    binstr = bin(xor)[2:].zfill(4)
    flag += binstr

print(flag)
for i in range(0, len(flag), 8):
    print(chr(int(flag[i : i + 8], 2)), end="")
