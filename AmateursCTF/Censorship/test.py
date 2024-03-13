test = "print(flag)"

enc = ""
for i in test:
    enc += f"chr({ord(i)}) + "

flag = "test"

code = enc[:-3]
code = ascii('\' + "Test" \' ')

print(code)
# exec(eval(code))
