dot = " "
arrow = "	"

with open("chall.txt", "r") as f:
    cipher = f.readlines()
    # for char in cipher:
    #     if char == dot:
    #         print(".", end="")
    #     elif char == arrow:
    #         print("-", end="")
    flag = ""
    for i in range(0, len(cipher), 2):
        binary = ""
        for char in cipher[i]:
            if char == dot:
                # print("0", end="")
                binary += "0"
            elif char == arrow:
                # print("1", end="")
                binary += "1"
        flag += chr(int(binary, 2))
    print(flag)
