enc = "3 81 17 37 27 63 25 54 93 0 124 68 43 22 35 103 45 12 42 23 111 103 80 45 30 1 100 45 3 73".split(
    " "
)

# flag = "TechnoFair11{"

# for i in range(len(flag)):
#     print(chr(int(enc[i]) ^ ord(flag[i])), end="")

key = "W4rMuP_"

flag = ""

for i in range(len(enc)):
    flag += chr(int(enc[i]) ^ ord(key[i % len(key)]))

print(flag)
