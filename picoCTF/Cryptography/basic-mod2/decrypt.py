with open("message.txt", "r") as f:
    arr = f.readline().split(" ")[:-1]
    flag = ""
    for num in arr:
        num = pow(int(num), -1, 41)
        if 1 <= num <= 26:
            flag += chr(ord("A") + num - 1)
        elif 27 <= num <= 36:
            flag += str(num - 27)
        else:
            flag += "_"

    print(flag)
