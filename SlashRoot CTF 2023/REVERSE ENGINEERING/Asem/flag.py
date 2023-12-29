decoded_flag = [
    "s",
    "}",
    "l",
    "h",
    "a",
    "u",
    "s",
    "p",
    "h",
    "3",
    "r",
    "5",
    "o",
    "_",
    "o",
    "h",
    "t",
    "u",
    "7",
    "p",
    "{",
    "_",
    "p",
    "u",
    "3",
    "l",
    "m",
    "u",
    "4",
    "d",
    "n",
    "_",
    "4",
    "n",
    "s",
    "4",
]

flag = ""
for i in range(0, len(decoded_flag), 2):
    flag += decoded_flag[i]

for i in range(len(decoded_flag) - 1, 0, -2):
    flag += decoded_flag[i]

print(flag)
