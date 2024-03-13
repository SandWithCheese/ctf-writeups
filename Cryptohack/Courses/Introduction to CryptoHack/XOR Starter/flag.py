text = "label"

decrypted = ""
for char in text:
    flag = ord(char) ^ 13
    decrypted += chr(flag)

print("crypto{" + decrypted + "}")
