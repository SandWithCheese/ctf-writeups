ciphertext = "610c6115651072014317463d73127613732c73036102653a6217742b701c61086e1a651d742b69075f2f6c0d69075f2c690e681c5f673604650364023944"

for i in range(0, len(ciphertext), 4):
    hexcode = ciphertext[i : i + 2]
    hexcipher = ciphertext[i + 2 : i + 4]
    xor = hex(int(hexcode, 16) ^ int(hexcipher, 16))[2:]
    print(
        bytes.fromhex(hexcode).decode("utf-8") + bytes.fromhex(xor).decode("utf-8"),
        end="",
    )
