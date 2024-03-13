# 2D = -
# 2E = .
# 20 = space

morse = """2D 2E 2D 2E  20 2D 2D 2D  20 2D 2D 20  2E 2D 2D 2E  
   20 2E 2E 2D  2E 20 2E 20  2E 2E 2E 20  2D 20 2E 2D  
   2D 2D 2D 20  2E 2E 2E 2E  2E 20 2D 2E  2E 20 2D 2D  
   2D 2E 2E 20  2D 2D 2E 2E  20 2D 20 2D  2D 2D 2D 2D  
   20 2E 2E 2E  2D 2D 20 2D  2D 2E 2D 20  2D 2D 2E 2E  
   20 2E 2E 20  2E 2E 2D 20  2D 2E 2E 2E  20 2E 2E 2E  
   2D 2D 20 2D  2D 2E 20 2E  2D 2E 20 2D  2D 2E 2E 20 
   2E 2E 2D 2E  20 2E 2E 2E  20 2D 2E 2D  2E 20 2D 2E  
  2D 20 2E 2E  2E 2D""".split()

flag = ""

for code in morse:
    if code == "2D":
        flag += "-"
    elif code == "2E":
        flag += "."
    elif code == "20":
        flag += " "

print(flag)
