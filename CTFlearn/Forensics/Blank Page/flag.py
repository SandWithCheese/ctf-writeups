with open("TheMessage.txt", "r") as f:
    data = f.read()

flag = ""
for i in data:
    if i == " ":
        flag += "0"
    else:
        flag += "1"

for i in range(0, len(flag), 8):
    print(chr(int(flag[i : i + 8], 2)), end="")
