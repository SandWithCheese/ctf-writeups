import numpy as np


def gauss_reduction(v: list, u: list):
    v1 = np.array(v)
    v2 = np.array(u)
    while True:
        if np.linalg.norm(v2) < np.linalg.norm(v1):
            v1, v2 = v2, v1

        m = round(v1.dot(v2) / v1.dot(v1))
        if m == 0:
            return v1, v2

        v2 = v2 - m * v1


v = [846835985, 9834798552]
u = [87502093, 123094980]

v1, v2 = gauss_reduction(v, u)

print(v1.dot(v2))
