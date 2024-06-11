key = "findit"
key += "2024"

# Constant list of integers
flag_enc = [
    32,
    0,
    0,
    0,
    32,
    32,
    113,
    100,
    116,
    79,
    4,
    89,
    2,
    80,
    54,
    66,
    83,
    92,
    3,
    107,
    8,
    80,
    9,
    11,
    54,
    16,
    93,
    1,
    83,
    90,
    82,
    7,
    49,
    80,
    80,
    71,
    10,
    1,
    1,
    73,
]


def xor(pt, key):
    return [pt[i] ^ key[i % len(key)] for i in range(len(pt))]


key_arr = []
for character in key:
    character = ord(character)
    key_arr.append(character)

flag_dec = xor(flag_enc, key_arr)

flag_dec_text = "".join(map(chr, flag_dec))

print(flag_dec_text)
