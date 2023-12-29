decrypted = "=KENv1a3]^_-^40a003\4/033]0111a_a.]x"

for char in decrypted:
    print(rf"{chr(ord(char) + 5)}", end="")
