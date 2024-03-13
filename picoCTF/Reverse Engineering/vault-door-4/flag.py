myBytes = [
    106,
    85,
    53,
    116,
    95,
    52,
    95,
    98,
    0x55,
    0x6E,
    0x43,
    0x68,
    0x5F,
    0x30,
    0x66,
    0x5F,
    "0142",
    "0131",
    "0164",
    "063",
    "0163",
    "0137",
    "0146",
    "064",
    "a",
    "8",
    "c",
    "d",
    "8",
    "f",
    "7",
    "e",
]

flag = "picoCTF{"
for i in range(16):
    flag += chr(myBytes[i])

for i in range(16, 24):
    flag += chr(int(myBytes[i], 8))

for i in range(24, 32):
    flag += myBytes[i]

print(flag + "}")
