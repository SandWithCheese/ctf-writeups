import sys

sys.set_int_max_str_digits(100_000)

import pwn
import numpy as np
from scipy import linalg

conn = pwn.remote("ctf-gemastik.ub.ac.id", 10000)
k = int(conn.recvline().decode()[3:].strip())
while k != 20:
    conn.close()
    conn = pwn.remote("ctf-gemastik.ub.ac.id", 10000)
    k = int(conn.recvline().decode()[3:].strip())

print(f"{k=}")
xs = []
ys = []
for i in range(k - 1):
    x, y = conn.recvline().decode().strip().strip("()").split(",")
    xs.append(int(x))
    ys.append(int(y))

for i in range(k - 1):
    print("-" * 16)
    print(f"{xs[i]=}")
    # print(f"{ys[i]=}")
    print("-" * 16)

# new_xs = []
# new_ys = []
# for i in range(len(xs) - 1):
#     pass

polynoms = []
for x in xs:
    coeff = []
    for i in range(k):
        coeff.append(pow(x, i))
    # print(coeff)
    polynoms.append(coeff)
    # break

new_polynoms = []
new_ys = []
for i in range(len(polynoms) - 1):
    new_coeff = []
    for j in range(len(polynoms[i])):
        if polynoms[i][j] - polynoms[i + 1][j] != 0:
            new_coeff.append(polynoms[i][j] - polynoms[i + 1][j])
    new_polynoms.append(new_coeff)
    new_ys.append(ys[i] - ys[i + 1])

new_coeff = []
for i in range(len(polynoms[0])):
    if polynoms[0][i] - polynoms[-1][i] != 0:
        new_coeff.append(polynoms[0][i] - polynoms[-1][i])

new_polynoms.append(new_coeff)
new_ys.append(ys[0] - ys[-1])

# for i in new_polynoms:
#     print(len(i))

# print(len(new_polynoms))

# A = np.array(new_polynoms)
# b = np.array(new_ys)
# inv_A = np.linalg.inv(A)
# x = inv_A.dot(b)
# print(x)

# print(len(A))
# for i in range(len(A)):
#     print(len(A[i]))
# print(len(b))
# print(type(new_polynoms))
# print(type(b))

# a = np.array([[3, 2, 0], [1, -1, 0], [0, 5, 1]])
# b = np.array([2, 4, -1])

# c = linalg.solve(new_polynoms, new_ys)
# print(c)

# c = np.linalg.solve(A, b)
# print(c)
# print(conn.recvline())
# print(len(xs))
# print(conn.recvline())
# conn.recvline()

# conn.interactive()
