local_38 = "cdbea780b4afc483b7afb4be84afa0c5afc09dc59acb96a493a0"

flag = ""
for i in range(0, len(local_38), 2):
    block = local_38[i : i + 2]
    flag += chr(int(block, 16) - 80)

print(flag[::-1])
