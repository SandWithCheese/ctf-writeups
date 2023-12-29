encrypted = "GUOXihf9j=:6i<8;;hfk;j:h=k8:7f<>596h"
flag = ""

for i in encrypted:
    flag += chr(ord(i) - 5)

print(flag)