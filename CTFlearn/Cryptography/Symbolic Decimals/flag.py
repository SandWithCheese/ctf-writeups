mapped = "!@#$%^&*()"

text = "^&,*$,&),!@#,*#,!!^,(&,!!$,(%,$^,(%,*&,(&,!!$,!!%,(%,$^,(%,&),!!!,!!$,(%,$^,(%,&^,!)%,!)@,!)!,!@%"
text = text.split(",")

flag = []
for i in text:
    chars = ""
    for char in i:
        if char == ")":
            chars += "0"
        else:
            chars += str(mapped.index(char) + 1)
    flag.append(chars)

for i in flag:
    print(chr(int(i)), end="")
