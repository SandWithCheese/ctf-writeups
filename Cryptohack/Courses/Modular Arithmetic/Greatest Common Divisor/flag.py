# Euclidean Algorithm
def gcd(A: int, B: int) -> int:
    if A == 0:
        return B
    if B == 0:
        return A

    return gcd(B, A % B)


print(gcd(66528, 52920))
