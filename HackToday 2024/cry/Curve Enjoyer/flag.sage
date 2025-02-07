def check_point_on_curve(p, a, b, x, y):
    curve = EllipticCurve(GF(p), [a, b])
    try:
        P = curve(x, y)
        return True
    except ValueError:
        return False


def attack(p, a, b, P, Q):
    # Create the elliptic curve over GF(p)
    curve = EllipticCurve(GF(p), [a, b])

    # Convert P and Q to points on the curve
    P = curve(P)
    Q = curve(Q)

    # Solve the discrete logarithm problem: find flag such that Q = P * flag
    flag = discrete_log(Q, P, operation="+")
    return flag


# Example usage based on challenge:
p = 47  # Example small prime
a = 3  # Curve parameter
b = 10  # Curve parameter
P = (10, 14)  # Example point P
Q = (26, 39)  # Example point Q = P * flag

# First, check if P and Q lie on the curve
if not check_point_on_curve(p, a, b, *P):
    print("P does not lie on the curve")
elif not check_point_on_curve(p, a, b, *Q):
    print("Q does not lie on the curve")
else:
    # Attack to recover the flag
    flag = attack(p, a, b, P, Q)
    print("Recovered flag:", flag)
