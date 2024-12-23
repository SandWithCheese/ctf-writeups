temp = "asdghkashdfclkamsdfjalxsdkjfxhcaksvjnalsckuqpoiewt"

local_148 = ""
for i in range(0, 350, 7):
    local_148 += temp[i % len(temp)]

assert len(local_148) == 50

key = [
    0x1A,
    0x1B,
    8,
    7,
    0xB,
    0x19,
    0x2A,
    0x18,
    0x55,
    0x5E,
    0x15,
    0x39,
    0x15,
    3,
    0x43,
    7,
    0,
    0x35,
    0x18,
    0x40,
    0x15,
    0x56,
    0x1A,
    0x56,
    0x55,
    0x34,
    0x58,
    0x1D,
    0x50,
    0x56,
    8,
    0x57,
    0x57,
    0x13,
    0x5D,
    1,
    0x5D,
    0x3B,
    0x4A,
    0x43,
    0x53,
    5,
    0x12,
    10,
    0xD,
    0x32,
    0x3B,
    0x3C,
    0x28,
    0xC,
]

user_input = local_148

local_108 = ""
for i in range(50):
    local_108 += chr(ord(user_input[i]) ^ key[i])

assert len(local_108) == 50

print(f"slashroot8{local_108}")
