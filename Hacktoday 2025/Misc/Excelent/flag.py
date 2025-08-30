from z3 import Solver, Int, sat

s = Solver()

# Declare variables
E = {i: Int(f"E{i}") for i in range(5, 14)}
F = {i: Int(f"F{i}") for i in range(5, 14)}
G = {i: Int(f"G{i}") for i in range(5, 14)}

E5, E6, E7, E8, E9, E10, E11, E12, E13 = [E[i] for i in range(5, 14)]
F5, F6, F7, F8, F9, F10, F11, F12, F13 = [F[i] for i in range(5, 14)]
G5, G6, G7, G8, G9, G10, G11, G12, G13 = [G[i] for i in range(5, 14)]

# Equations
s.add(8 * E5 + 7 * F13 - 10 * F6 + 6 * G11 == 112)
s.add(5 * E10 + 8 * E9 + F13 + 3 * F6 - 5 * G12 == -13)
s.add(10 * E9 - 8 * F11 + 8 * G11 + 9 * G7 == 106)
s.add(-E5 - 7 * E9 - 8 * F11 - 2 * F12 + G9 == -127)
s.add(-10 * E12 + 10 * E6 - 7 * E9 + 5 * F13 + 2 * G13 == 280)
s.add(-3 * E12 - 3 * F13 - 8 * F5 - 7 * F6 - 5 * F9 == -376)
s.add(-3 * E9 + 4 * F11 + 9 * F6 - 4 * F9 + 3 * G6 == 40)
s.add(10 * F11 - 9 * F8 + 2 * F9 + G10 - 3 * G5 == 0)
s.add(-4 * E7 - 2 * G12 + 3 * G13 + 8 * G7 + 3 * G9 == -34)
s.add(-8 * E5 + 7 * F10 + 8 * F12 - 4 * F8 - 10 * G11 == 347)
s.add(5 * E10 + 3 * E12 + 8 * E5 + 10 * F8 + 5 * G10 == 245)
s.add(9 * E6 - F10 + F12 + 6 * F5 + G7 == 406)
s.add(-5 * E8 - 6 * E9 + 6 * F11 + 4 * F12 == 163)
s.add(-4 * F11 - 7 * F13 - 4 * F5 + 8 * G11 == -92)
s.add(6 * E10 - 4 * E9 - F10 - 3 * G9 == 23)
s.add(6 * E11 - 5 * E5 + 8 * F12 - 9 * G8 - 2 * G9 == 212)
s.add(5 * E11 - 2 * E12 - 10 * E13 + 8 * F13 + 6 * G13 == 317)
s.add(-8 * E10 - 7 * E7 - 2 * E9 + 4 * F13 - 3 * G8 == -350)
s.add(-10 * F11 - 3 * F12 + 6 * F6 + G12 + 8 * G8 == 91)
s.add(9 * E5 - 3 * F11 + 7 * F7 + 10 * F8 - 7 * G6 == -99)
s.add(-6 * E11 + 9 * E8 + 6 * F13 - 4 * F5 - 9 * G5 == -385)
s.add(-7 * E10 + 4 * E6 - 5 * F13 + 10 * F5 - 7 * G13 == 7)
s.add(5 * E12 - 6 * E7 + 8 * F7 + 8 * G13 - 7 * G5 == -115)
s.add(-6 * E12 + 5 * E7 - 10 * F10 + 6 * F11 + F6 == -190)
s.add(8 * E6 + 3 * F11 - 7 * F9 + 8 * G10 + 2 * G8 == 233)
s.add(-9 * F10 - 2 * F11 + 8 * F6 + 5 * F8 - 4 * G5 == -322)
s.add(2 * E10 - 7 * E11 - 5 * E13 - 5 * E9 - G12 == -245)

# Range constraints for modulo 37
for var in list(E.values()) + list(F.values()) + list(G.values()):
    s.add(var >= 0, var < 37)

# Solve
if s.check() == sat:
    m = s.model()
    print("Solution:")
    order = (
        [E[i] for i in range(5, 14)]
        + [F[i] for i in range(5, 14)]
        + [G[i] for i in range(5, 14)]
    )
    values = [m.evaluate(v).as_long() for v in order]
    values_a = values[:9]
    values_b = values[9:18]
    values_c = values[18:]

    def convert(x):
        if (x >= 0) and (x < 10):
            return str(x)
        elif x == 10:
            return "_"
        else:
            return chr(x + 86)

    flag = ""
    for i in range(9):
        for a in range(37):
            for b in range(37):
                for c in range(37):
                    if ((2 * a + 4 * b + 5 * c) % 37 == values_a[i]) and (
                        ((9 * a + 2 * b + 1 * c) % 37 == values_b[i])
                        and (((3 * a + 17 * b + 7 * c) % 37 == values_c[i]))
                    ):
                        flag += convert(a)
                        flag += convert(b)
                        flag += convert(c)

    print(flag)
else:
    print("No solution found.")
