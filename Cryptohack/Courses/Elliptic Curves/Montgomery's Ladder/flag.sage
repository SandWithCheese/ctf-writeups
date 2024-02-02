F.<x> = Zmod(pow(2, 255) - 19)[]
E = EllipticCurve(F, [0, 486662, 0, 1, 0])

G_x = 9
nA = 0x1337c0decafe

G_y_2 = (pow(G_x, 3) + 486662 * pow(G_x, 2) + G_x) % (pow(2, 255) - 19)

f = x^2 - G_y_2
ys = [i[0] for i in f.roots()]

F = Zmod(pow(2, 255) - 19)
E = EllipticCurve(F, [0, 486662, 0, 1, 0])

for y in ys:
    G = E([G_x, y])

    Q = nA * G
    print(f"Found: {Q[0]}")
    break