decrypted = "GUOV~<4<`2<273d477161ddga06=7gga33=a<x"

for char in decrypted:
    print(chr(ord(char) ^ 5), end="")
