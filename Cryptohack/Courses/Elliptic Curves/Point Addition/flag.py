a = 497
b = 1768
p = 9739

P = (493, 5564)
Q = (1539, 4742)
R = (4403, 5202)


def point_addition(P: tuple[int], Q: tuple[int]) -> tuple[int]:
    O = (0, 0)

    if P == O:
        return Q
    elif Q == O:
        return P

    if P[0] == Q[0] and P[1] == -Q[1]:
        return O

    if P != Q:
        lam = (Q[1] - P[1]) * pow(Q[0] - P[0], -1, p)
    else:
        lam = (3 * pow(P[0], 2) + a) * pow(2 * P[1], -1, p)

    x = (pow(lam, 2) - P[0] - Q[0]) % p
    y = (lam * (P[0] - x) - P[1]) % p

    return (x, y)


S = point_addition(P, point_addition(P, point_addition(Q, R)))

print(f"Flag: {S}")
