enc_flag = [
    110,
    102,
    118,
    102,
    115,
    114,
    118,
    130,
    103,
    104,
    92,
    80,
    98,
    108,
    63,
    63,
    65,
    112,
    113,
    144,
]


for i in range(len(enc_flag)):
    print(chr(enc_flag[i] - i), end="")

