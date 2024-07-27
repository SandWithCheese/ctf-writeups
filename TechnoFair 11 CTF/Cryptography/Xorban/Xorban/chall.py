import random

# from secret import flag
flag = [11, 11, 11, 11, 11]

key = [random.randint(1, 256) for _ in range(len(flag))]
print(f"{key=}")

xorban = []
enc = []
for i, v in enumerate(key):
    k = 1
    print(k)
    for j in range(i, 0, -1):
        k ^= key[j]
        print(key[j])
    print()
    xorban.append(k)
    enc.append(flag[i] ^ v)

# with open("output.txt", "w") as f:
#     f.write(f"{xorban=}\n")
#     f.write(f"{enc=}\n")

print(f"{xorban=}")
print(f"{enc=}")

# xorban[0] = 1
# xorban[1] = key[1] ^ 1
# if key[1] odd, xorban[1] = key[1] ^ 1 = key[1] - 1
# if key[1] even, xorban[1] = key[1] ^ 1 = key[1] + 1

# other way around
# if xorban[1] odd, key[1] = xorban[1] - 1
# if xorban[1] even, key[1] = xorban[1] + 1

# xorban[2] = key[2] ^ key[1] ^ 1
# if xorban[2] odd, key[2] = xorban[2] ^ key[1] ^ 1 = xorban[2] - key[1] + 1
# if xorban[2] even, key[2] = xorban[2] ^ key[1] ^ 1 = xorban[2] - key[1] - 1

# etc
