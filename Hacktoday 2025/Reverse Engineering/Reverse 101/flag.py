from collections import defaultdict

# Replace with the actual lookup_table from the ELF
lookup_table = [
    234,
    9,
    103,
    60,
    5,
    79,
    232,
    229,
    45,
    51,
    131,
    3,
    168,
    29,
    170,
    216,
    99,
    161,
    111,
    204,
    220,
    209,
    78,
    89,
    72,
    191,
    157,
    119,
    226,
    184,
    244,
    134,
    21,
    61,
    175,
    15,
    223,
    100,
    230,
    28,
    128,
    185,
    84,
    208,
    164,
    44,
    113,
    105,
    27,
    85,
    203,
    146,
    153,
    130,
    66,
    42,
    250,
    140,
    174,
    133,
    115,
    4,
    52,
    73,
    65,
    10,
    104,
    238,
    30,
    211,
    46,
    121,
    2,
    190,
    159,
    172,
    112,
    156,
    95,
    47,
    124,
    177,
    77,
    202,
    81,
    38,
    123,
    13,
    182,
    242,
    64,
    33,
    225,
    0,
    241,
    122,
    210,
    37,
    106,
    163,
    82,
    98,
    34,
    218,
    187,
    214,
    125,
    132,
    120,
    219,
    252,
    32,
    135,
    215,
    245,
    48,
    198,
    222,
    76,
    231,
    213,
    192,
    227,
    144,
    19,
    152,
    110,
    12,
    217,
    126,
    196,
    201,
    248,
    148,
    109,
    138,
    63,
    249,
    200,
    36,
    197,
    101,
    127,
    145,
    149,
    54,
    16,
    167,
    102,
    80,
    239,
    181,
    14,
    83,
    224,
    142,
    69,
    176,
    118,
    171,
    251,
    136,
    43,
    246,
    155,
    18,
    165,
    68,
    53,
    90,
    94,
    41,
    93,
    162,
    116,
    212,
    205,
    25,
    235,
    193,
    74,
    58,
    169,
    199,
    17,
    180,
    49,
    147,
    92,
    158,
    160,
    75,
    141,
    20,
    96,
    31,
    137,
    117,
    186,
    11,
    67,
    233,
    88,
    91,
    24,
    97,
    237,
    247,
    86,
    195,
    236,
    39,
    221,
    87,
    240,
    178,
    40,
    206,
    194,
    1,
    207,
    71,
    150,
    114,
    56,
    107,
    243,
    179,
    166,
    183,
    50,
    143,
    254,
    154,
    129,
    59,
    55,
    23,
    7,
    8,
    108,
    151,
    22,
    139,
    228,
    253,
    173,
    26,
    188,
    35,
    255,
    62,
    70,
    189,
    6,
    57,
]

# Reverse lookup table
reverse_lookup = {val: idx for idx, val in enumerate(lookup_table)}


def ror(val, r_bits):
    return ((val & 0xFF) >> r_bits) | ((val << (8 - r_bits)) & 0xFF)


def inv_rol1(val):
    return ror(val, 1)


def inv_xor3c(val):
    return val ^ 0x3C


def inv_rol3(val):
    return ror(val, 3)


def inv_xor_a5(val):
    return val ^ 0xA5


def inv_swap_nibble(val):
    return ((val & 0x0F) << 4) | ((val & 0xF0) >> 4)


def inv_addpos(val, pos):
    return (val - (pos % 0x11)) % 0x100


def inv_not(val):
    return (~val) & 0xFF


def inv_lookup(val):
    return reverse_lookup[val]


def inv_keyxor(val, pos):
    return val ^ ((pos * 7 + 0xB) % 0x100)


def inv_rol(val, pos):
    return ror(val, pos % 8)


def inv_rot13(val):
    if 0x61 <= val <= 0x7A:
        return (val - 0x61 - 13) % 26 + 0x61
    elif 0x41 <= val <= 0x5A:
        return (val - 0x41 - 13) % 26 + 0x41
    else:
        return val


def inv_shift(val, pos):
    return ((val - 0x20 - ((pos * 5 + 3) % 0x5E)) % 0x5E) + 0x20


def reverse_full_transform(v, pos):
    v = inv_rol1(v)
    v = inv_xor3c(v)
    v = inv_rol3(v)
    v = inv_xor_a5(v)
    v = inv_swap_nibble(v)
    v = inv_addpos(v, pos)
    v = inv_not(v)
    v = inv_lookup(v)
    v = inv_keyxor(v, pos)
    v = inv_rol(v, pos)
    v = inv_rot13(v)
    v = inv_shift(v, pos)
    return v


# The expected values we calculated from reversing each check function
expected_values = [
    1,
    158,
    125,
    131,
    107,
    115,
    0x90,
    14,
    43,
    201,
    0xE8,
    0xAC,
    0x8D,
    35,
    110,
    0xFE,
    0,
    103,
    208,
    87,
    68,
    86,
    14,
    0xB2,
    227,
    137,
    114,
    46,
    231,
    89,
    151,
    1,
    0x85,
    0xC6,
    200,
    104,
    105,
    34,
    29,
    54,
    34,
    0x80,
    0x96,
    0xD4,
    34,
    115,
    109,
    75,
    245,
    9,
    64,
    11,
    245,
    114,
    221,
    111,
    37,
    0xD1,
    122,
    122,
    63,
    252,
    0xC1,
    241,
    164,
    0xC0,
    5,
    216,
    195,
    5,
    51,
    247,
    152,
    109,
    30,
    0xA5,
    188,
    0xE5,
    166,
    0xB2,
    0xBF,
    91,
    193,
    16,
    72,
    27,
]

flag = "".join(
    chr(reverse_full_transform(v, i + 1)) for i, v in enumerate(expected_values)
)
print("Flag:", flag)
