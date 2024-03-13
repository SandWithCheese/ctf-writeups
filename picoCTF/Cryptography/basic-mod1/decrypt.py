with open("message.txt", "r") as f:
    arr = f.readline().split(" ")[:-1]
    flag = ""
    for num in arr:
        num = int(num) % 37
        if 0 <= num <= 25:
            flag += chr(ord("A") + num)
        elif 26 <= num <= 35:
            flag += str(num - 26)
        else:
            flag += "_"

    print(flag)
