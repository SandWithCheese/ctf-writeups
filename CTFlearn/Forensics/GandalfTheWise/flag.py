from base64 import b64decode

test1 = "xD6kfO2UrE5SnLQ6WgESK4kvD/Y/rDJPXNU45k/p"
test2 = "h2riEIj13iAp29VUPmB+TadtZppdw3AuO7JRiDyU"

test1 = b64decode(test1)
test2 = b64decode(test2)

flag = ""
for i in range(len(test1)):
    flag += chr(test1[i] ^ test2[i])

print(flag)
