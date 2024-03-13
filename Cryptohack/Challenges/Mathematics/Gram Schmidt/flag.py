def v_mult(v1, v2):
    res = 0
    for i in range(len(v1)):
        res += v1[i] * v2[i]
    return res


def scale_mult(v, scale):
    for i in range(len(v)):
        v[i] *= scale
    return v


# def v_size(v):
#     return pow(v_mult(v, v), 0.5)


def v_add(u, v):
    for i in range(len(u)):
        u[i] += v[i]
    return u


def v_subs(u, v):
    for i in range(len(u)):
        u[i] -= v[i]
    return u


def proj(u, v):
    scale = v_mult(v, u) / v_mult(u, u)
    return scale_mult(u, scale)


def gram_schmidt(v: list):
    u = [0 for _ in v]
    u[0] = v[0]
    for i in range(1, len(v)):
        tmp_v = [0 for _ in range(len(v[i]))]
        for j in range(i):
            tmp_v = v_add(tmp_v, proj(u[j], v[i]))
        u[i] = v_subs(v[i], tmp_v)

    return u


v1 = [4, 1, 3, -1]
v2 = [2, 1, -3, 4]
v3 = [1, 0, -2, 7]
v4 = [6, 2, 9, -5]

v = [v1, v2, v3, v4]
gs = gram_schmidt(v)
print(gs)

import numpy as np


# def gram_schmidt(A):
#     (n, m) = A.shape

#     for i in range(m):
#         q = A[:, i]  # i-th column of A

#         for j in range(i):
#             q = q - np.dot(A[:, j], A[:, i]) * A[:, j]

#         if np.array_equal(q, np.zeros(q.shape)):
#             raise np.linalg.LinAlgError(
#                 "The column vectors are not linearly independent"
#             )

#         # normalize q
#         q = q / np.sqrt(np.dot(q, q))

#         # write the vector back in the matrix
#         A[:, i] = q


# np_vs = np.array(vs)
# print(np_vs)
# gram_schmidt(np_vs)
