from z3 import *

values = []
with open("code.txt", "r") as f:
    for line in f:
        values.append(
            int(line.strip().split("==")[-1].strip().split(" ")[0].split(")")[0], 16)
        )

dat = {}
with open("dat.txt", "r") as f:
    for line in f:
        addr, hex_val = line.strip().split(" ")
        dat[int(addr, 16)] = int(hex_val, 16)

base = 0x00103020

print(dat)

s = Solver()

param_1 = [BitVec("param_1_%i" % i, 8) for i in range(0x48)]

power = 2
for i in range(0x48):
    if i == pow(2, power) - 1:
        # s.add(((param_1[i] << power) ^ param_1[i]) == values[i])
        s.add((dat[base + param_1[i]] << power) ^ param_1[i] == values[i])
        power += 1
    else:
        # s.add(((param_1[i] * (i + 1)) ^ param_1[i]) == values[i])
        s.add((dat[base + param_1[i]] * (i + 1)) ^ param_1[i] == values[i])

print(s)

# if s.check() == sat:
#     m = s.model()
#     flag = ""
#     for i in range(0x48):
#         flag += chr(m[param_1[i]].as_long())
#     print(flag)
# else:
#     print("unsat")
