from math import prod
from Crypto.Util.number import inverse


# Euclidean Algorithm
def gcd(A: int, B: int) -> int:
    if A == 0:
        return B
    if B == 0:
        return A

    return gcd(B, A % B)


# GCD of many numbers
def gcd_n(arr: list[int]) -> int:
    length = len(arr)
    if length == 0:
        return 0

    temp = arr[0]
    for i in range(1, length):
        temp = gcd(temp, arr[i])

    return temp


def crt(arr_a: list[int], arr_m: list[int]) -> int:
    if gcd_n(arr_m) != 1 or (len(arr_a) != len(arr_m)):
        return -1

    M = prod(arr_m)

    x = 0
    for i in range(len(arr_a)):
        m_n = M // arr_m[i]
        m_inv_n = inverse(m_n, arr_m[i])

        x += arr_a[i] * m_n * m_inv_n

    return x % M


print(crt([2, 3, 5], [5, 11, 17]))
