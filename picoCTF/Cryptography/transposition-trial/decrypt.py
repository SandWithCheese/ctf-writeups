with open("message.txt", "r") as f:
    flag = f.readline()
    print(flag)
    decoded_flag = ""
    sub_flag = ""
    for i in range(1, len(flag) + 1):
        if i % 3 == 0:
            sub_flag = flag[i - 1] + sub_flag
            decoded_flag += sub_flag
            sub_flag = ""
        else:
            sub_flag += flag[i - 1]

    print(decoded_flag)
