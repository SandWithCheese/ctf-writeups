x_0 = 1096770097
x_1 = 1952395366
x_2 = 1600270708
x_3 = 1601398833
x_4 = 1716808014
x_5 = 1734293296
x_6 = 842413104
x_7 = 1684157793

hex_x_0 = hex(x_0)[2:]
hex_x_1 = hex(x_1)[2:]
hex_x_2 = hex(x_2)[2:]
hex_x_3 = hex(x_3)[2:]
hex_x_4 = hex(x_4)[2:]
hex_x_5 = hex(x_5)[2:]
hex_x_6 = hex(x_6)[2:]
hex_x_7 = hex(x_7)[2:]

print("picoCTF{", end="")
for i in range(0, len(hex_x_0), 2):
    print(chr(int(hex_x_0[i : i + 2], 16)), end="")
for i in range(0, len(hex_x_1), 2):
    print(chr(int(hex_x_1[i : i + 2], 16)), end="")
for i in range(0, len(hex_x_2), 2):
    print(chr(int(hex_x_2[i : i + 2], 16)), end="")
for i in range(0, len(hex_x_3), 2):
    print(chr(int(hex_x_3[i : i + 2], 16)), end="")
for i in range(0, len(hex_x_4), 2):
    print(chr(int(hex_x_4[i : i + 2], 16)), end="")
for i in range(0, len(hex_x_5), 2):
    print(chr(int(hex_x_5[i : i + 2], 16)), end="")
for i in range(0, len(hex_x_6), 2):
    print(chr(int(hex_x_6[i : i + 2], 16)), end="")
for i in range(0, len(hex_x_7), 2):
    print(chr(int(hex_x_7[i : i + 2], 16)), end="")
print("}")
