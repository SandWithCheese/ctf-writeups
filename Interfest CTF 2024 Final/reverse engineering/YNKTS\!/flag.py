from pwn import xor

with open("trap", "rb") as f:
    test = f.read()

# test = b"\x30\x19\x4b\x59\x29\x0a\x41\x0d\x11\x16\x10\x0f\x07\x2f\x4b\x2a\x05\x45\x58\x25\x09\x16\x33\x31\x28\x26\x3a\x51\x54\x4f\x32\x30\x52\x3b\x4c\x31\x04\x1d\x54\x53\x0f\x08\x0d\x02\x38\x01\x5f\x3b\x3d\x45\x22\x2a\x43\x42\x14\x1c\x32\x0b\x3c\x35\x2a\x44\x41\x14\x02\x5e\x3d\x3e\x06\x00\x5e\x32\x32\x48\x1f\x2f\x1b\x04\x56\x14\x53\x0e\x1f\x02\x48\x3d\x59\x14\x37\x25\x1c\x46\x41\x31\x28\x16\x16\x38\x10\x19\x12\x54\x3e\x2e\x44\x0c\x52\x3c\x2b\x44\x0f\x26\x12\x19\x02\x37\x2b\x24\x21\x5a\x48\x45\x22\x4c\x34\x44\x39\x4b\x43\x5b\x39\x2c\x5a\x16\x56\x36\x58\x22\x43\x4a\x16\x40\x35\x00\x0c\x41\x27\x1f\x20\x39\x01\x54\x04\x24\x09\x40\x3b\x3f\x4c\x0a\x52\x52\x2d\x2e\x49\x18\x55\x09\x37\x2d\x0c\x42\x0a\x57\x1a\x08\x32\x4a\x4e\x33\x4b\x54\x04\x39\x34\x27\x4e\x49\x28\x59\x5d\x11\x5f\x22\x36\x3c\x4a\x0d\x11\x1d"


for i in range(1, 256):
    flag = xor(test, i)

    print(f"{i}: {flag}")
# with open("flag", "wb") as f:
#     f.write(flag)

mapping = {
    "7F": "f",
    "6p": "o",
    "7r": "r",
    "6s": "e",
    "7s": "s",
    "7t": "t",
    "7y": "y",
    "7C": "c",
    "7{": "{",
    "7}": "}",
    "7_": "_",
    "6t": "a",
    "6q": "i",
    "7M": "M",
    "7V": "V",
    "7P": "P",
    "7G": "G",
    "7u": "u",
    "7T": "T",
    "7h": "h",
    "7V": "V",
    "7N": "N",
    "7n": "n",
    "7I": "I"
}

# enc = "7F6p7r6s7s7t7y7C7t7F7"
# enc = "ForestyCtF{MVP_aGuu_TahVN_inI}"
enc = "7F6p7r6s7s7t7y7C7t7F7{7M7V7P7_6t7G7u6u7_7T6t7h7V7N7_6q7n7I7}"

flag = ""
for i in range(0, len(enc), 2):
    block = enc[i: i+2]
    if block in mapping.keys():
        flag += mapping[block]

print(flag)