decrypted = "CQKRz2gd7636344gee496ee97c4gcbe5199|"

for char in decrypted:
    print(chr(ord(char) ^ 1), end="")
