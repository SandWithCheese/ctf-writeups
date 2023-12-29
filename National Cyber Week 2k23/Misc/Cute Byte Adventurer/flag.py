from string import hexdigits

with open("bc.txt", "r") as f:
    text = f.read()

new_text = ""
for i in range(0, len(text), 2):
    block = text[i : i + 2]
    if chr(int(block, 16)) in hexdigits:
        new_text += chr(int(block, 16))

for i in range(0, len(new_text), 2):
    block = new_text[i : i + 2]
    print(chr(int(block, 16)), end="")


# Kunci = 69
# encrypt_data = lambda data: print(
#     "0x" + bytearray([char + Kunci for char in bytes(data, "utf-8")]).hex()
# )
# encrypt_data(input("text-to-secure: "))
