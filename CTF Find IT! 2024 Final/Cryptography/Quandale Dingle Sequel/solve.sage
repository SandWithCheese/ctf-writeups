from Crypto.Util.number import *

x = [(1 << i) + i for i in range(100, 104)]
y = []

lines = open("../bin/out.txt", "r").readlines()
for line in lines:
    line = line.strip()
    if len(line) > 0:
        y.append(int(line))

ct = y[-1]
y = y[:-1]

'''
(Kx^4, Kx^3, Kx^2, Kx, K, -Ky) * (A, -B, C, -D, E, 1) = 0
'''
arr = [[0 for i in range(10)] for _ in range(6)]

for i in range(6):
    arr[i][i] = 1

for i in range(6, 10):
    cur_x = x[i-6]
    cur_y = y[i-6]
    for j in range(5):
        arr[j][i] = cur_x ^ (4-j)
    arr[-1][i] = -1 * cur_y

for k in range(0, 400):
    for i in range(6):
        for j in range(6, 10):
            arr[i][j] <<= 1
    M = Matrix(ZZ, arr)
    L = M.LLL()
    if L[0][5] == 1 and L[0][6] == 0:
        print("Found")
        E = abs(L[0][4])
        E = E ^ 4
        print(long_to_bytes(E ^^ ct))
        exit(0)

