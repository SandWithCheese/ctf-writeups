flag = "灩捯䍔䙻ㄶ形楴獟楮獴㌴摟潦弸弰㑣〷㘰摽"

# "".join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])

for i in range(len(flag)):
    ori_1 = ord(flag[i]) >> 8
    ori_2 = ord(flag[i]) - (ord(flag[i]) >> 8 << 8)
    print(chr(ori_1) + chr(ori_2), end="")
