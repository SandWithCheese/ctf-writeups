xorban = [
    1,
    243,
    128,
    75,
    251,
    28,
    249,
    9,
    231,
    152,
    154,
    2,
    237,
    223,
    175,
    17,
    5,
    150,
    118,
    14,
    173,
    151,
    242,
    240,
    176,
    10,
    209,
    29,
    236,
    208,
    222,
    177,
    183,
    91,
    162,
    8,
    12,
    103,
    221,
    30,
    119,
    184,
]
enc = [
    105,
    151,
    16,
    163,
    222,
    136,
    163,
    145,
    135,
    13,
    51,
    169,
    148,
    6,
    30,
    199,
    97,
    249,
    137,
    22,
    252,
    105,
    81,
    107,
    36,
    229,
    175,
    164,
    192,
    79,
    81,
    6,
    117,
    179,
    186,
    198,
    48,
    24,
    201,
    170,
    10,
    178,
]


# xorban[0] = 1
# xorban[1] = key[1] ^ 1
# if key[1] odd, xorban[1] = key[1] ^ 1 = key[1] - 1
# if key[1] even, xorban[1] = key[1] ^ 1 = key[1] + 1

# other way around
# if xorban[1] odd, key[1] = xorban[1] - 1
# if xorban[1] even, key[1] = xorban[1] + 1

# xorban[2] = key[2] ^ key[1] ^ 1
# if xorban[2] odd, key[2] = xorban[2] ^ key[1] ^ 1 = xorban[2] - key[1] + 1
# if xorban[2] even, key[2] = xorban[2] ^ key[1] ^ 1 = xorban[2] - key[1] - 1

# etc

key = []
for i, v in enumerate(xorban):
    if i == 0:
        # Temp
        key.append(1)
    else:
        # v = key[i] ^ key[i-1] ^ ... ^ 1
        # key[i] = v ^ key[i-1] ^ ... ^ 1

        # if v odd
        if v % 2 == 1:
            temp = 0
            # Loop over the generated key
            for j in range(i):
                temp ^= key[j]
            key.append(v ^ temp)
        else:
            temp = 0
            for j in range(i):
                temp ^= key[j]
            key.append(v ^ temp)

for i in range(256):
    key[0] = i

    dec = []
    for i, v in enumerate(enc):
        dec.append(v ^ key[i])

    flag = ""
    for i in dec:
        flag += chr(i)

    if flag.startswith("Techno"):
        print(flag)
        break
