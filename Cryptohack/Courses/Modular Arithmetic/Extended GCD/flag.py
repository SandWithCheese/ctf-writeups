def extendedGCD(a, b):
    if a == 0:
        return b, 0, 1

    gcd, s1, t1 = extendedGCD(b % a, a)

    s, t = updateCoeff(a, b, s1, t1)

    return gcd, s, t


def updateCoeff(a, b, s, t):
    return (t - (b // a) * s, s)


gcd, s, t = extendedGCD(26513, 32321)
print(gcd, s, t)
