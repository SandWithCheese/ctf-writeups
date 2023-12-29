with open("qr_code.txt", "r") as f:
    lines = f.readlines()

# binstr = ""
for line in lines:
    binstr = bin(int(line.strip()))[2:]
    for i in binstr:
        if i == "1":
            print(chr(9608), end="")
        else:
            print(" ", end="")
    print()

# print(len(binstr))
