hexcode = "50 43 54 46 7B 64 30 5F 79 30 55 5F 6B 4E 30 57 5F 68 30 57 5F 74 30 5F 52 33 34 44 5F 6D 30 72 35 33 5F 43 30 64 33 3F 7D".split()

for i in hexcode:
    print(chr(int(i, 16)), end="")
