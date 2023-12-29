encrypted = "GUOV~1da42=6623ad5f1gfc73=0d36<4ga2x"
flag = ""

for i in encrypted:
    flag += chr(ord(i) ^ 5)

print(flag)