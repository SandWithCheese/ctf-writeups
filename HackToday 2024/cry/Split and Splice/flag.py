from Crypto.Util.number import long_to_bytes


def grey_v2(x):
    n = x ^ (x // 2) ^ (x // 4)
    return n


def grey_v3(x):
    n = (2 * x) ^ (x) ^ (x // 2) ^ (x // 4)
    return n


with open("file.txt", "r") as f:
    ct = f.read().split("=")[1]

    n1 = ct[:111]
    n2 = ct[111:]


b1 = bin(int(n1))[2:]
b2 = bin(int(n2))[2:]

b1_ori = "1"
i = 1
while len(b1_ori) < len(b1):
    check = b1_ori + "0"

    for j in range(1000):
        check = bin(grey_v2(int(check, 2)))[2:]

    last_char = check[-1]
    if last_char == b1[i]:
        b1_ori += "0"
    else:
        b1_ori += "1"

    i += 1


temp_b2 = b2
for j in range(1000):
    b2_ori = "1"

    for i in range(1, 4):
        temp = temp_b2[i]
        for char in b2_ori:
            temp = bin(int(temp) ^ int(char))[2:]
        b2_ori += temp

    i = 4
    while len(b2_ori) < len(temp_b2):
        check = b2_ori + "0"

        check = (
            int(check, 2)
            ^ (int(check, 2) // 2)
            ^ (int(check, 2) // 4)
            ^ (int(check, 2) // 8)
        )

        check = bin(check)[2:]

        last_char = check[-1]
        if last_char == temp_b2[i]:
            b2_ori += "0"
        else:
            b2_ori += "1"

        i += 1

    temp_b2 = bin(int(b2_ori, 2) // 2)[2:]


print((long_to_bytes(int(b1_ori, 2)) + long_to_bytes(int(temp_b2, 2))).decode())
