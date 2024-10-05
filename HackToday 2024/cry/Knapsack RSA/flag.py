from Crypto.Util.number import long_to_bytes

with open("output.txt", "r") as f:
    ct = eval(f.readline().strip().split(" = ")[1])
    out = eval(f.readline().strip().split(" = ")[1])
    weight = eval(f.readline().strip().split(" = ")[1])
    sums = eval(f.readline().strip().split(" = ")[1])
    n = eval(f.readline().strip().split(" = ")[1])

binary = []
for i in range(len(out)):
    bin_str = ""
    for j in range(len(out[i])):
        if out[i][j].bit_length() >= 500 and out[i][j].bit_length() <= 520:
            bin_str += "0"
        else:
            bin_str += "1"
    binary.append(bin_str)

# flag1 = "".join(binary)
# flag1 = long_to_bytes(int(flag1, 2))

for b in binary:
    print(b)

key = 0
