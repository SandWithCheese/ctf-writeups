from string import hexdigits

def initialMagic(u):
    u ^= (u << 31) & 0xFFFFFFFFFFFFFFFF 
    u ^= (u >> 19)
    u ^= (u << 13) & 0xFFFFFFFFFFFFFFFF
    return u & 0xFFFFFFFFFFFFFFFF

for h in hexdigits:
    hexes = initialMagic(int(h*16, 16))
    binstr = bin(hexes)[2:].zfill(64)
    for i in range(0, 64, 8):
        print(binstr[i:i+8], end=' ')
    print()