a = 497
b = 1768
p = 9739

P = (2339, 2213)


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


def scalar_multiplication(n: int, P: tuple[int]) -> tuple[int]:
    R = (0, 0)
    Q = P

    while n > 0:
        if n % 2 == 1:
            R = point_addition(R, Q)
        Q = point_addition(Q, Q)
        n = n // 2

    return R


X = (5323, 5438)
assert scalar_multiplication(1337, X) == (1089, 6931)

print(scalar_multiplication(7863, P))
