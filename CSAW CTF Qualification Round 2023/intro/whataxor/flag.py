hexstr = "c9d9cbddc9deccd19ac4cff5d9c2cfcffaf59bddc5f5d9c2cffddaf598c2d8cfcff59fc2cfcfc1d9f5f5f5f5f5d0f5f5f5d0d0d0f5f5f5f5f5d0d0d0d0d0d0f5f5f5f5d2c5d8d7"
xor_value = int("aa", 16)

for i in range(0, len(hexstr), 2):
    block = hexstr[i : i + 2]
    print(chr(int(block, 16) ^ xor_value), end="")
