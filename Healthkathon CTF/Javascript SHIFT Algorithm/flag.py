decrypted = "CQKT|9685:e6gd:53216b5e3:75:35e3g177f~"
flag = ""

for i in decrypted:
    flag += chr(ord(i) - 1)

print(flag)