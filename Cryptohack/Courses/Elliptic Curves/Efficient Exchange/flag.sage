F.<x> = Zmod(9739)[]
E = EllipticCurve(F, [497, 1768])

q_x = 4726
nB = 6534

y_2 = (pow(q_x, 3, 9739) + 497 * q_x + 1768) % 9739
f = x^2 - y_2

ys = [i[0] for i in f.roots()]

F = Zmod(9739)
E = EllipticCurve(F, [497, 1768])

for y in ys:
    Q = E([q_x, y])

    S = nB * Q
    print(f"Found: {S[0]}")
    break
