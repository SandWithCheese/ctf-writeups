import random
from string import printable

# from secret import flag

rounds = 5
block_size = 8
sa = {
    0: 15,
    1: 2,
    2: 14,
    3: 0,
    4: 1,
    5: 3,
    6: 10,
    7: 6,
    8: 4,
    9: 11,
    10: 9,
    11: 7,
    12: 13,
    13: 12,
    14: 8,
    15: 5,
}
sb = {
    0: 12,
    1: 8,
    2: 13,
    3: 6,
    4: 9,
    5: 1,
    6: 11,
    7: 14,
    8: 5,
    9: 10,
    10: 3,
    11: 4,
    12: 0,
    13: 15,
    14: 7,
    15: 2,
}
key = [random.randrange(255), random.randrange(255)] * 4
to_bin = lambda x, n=block_size: format(x, "b").zfill(n)
to_int = lambda x: int(x, 2)
to_chr = lambda x: "".join([chr(i) for i in x])
to_ord = lambda x: [ord(i) for i in x]
bin_join = lambda x, n=int(block_size / 2): (str(x[0]).zfill(n) + str(x[1]).zfill(n))
bin_split = lambda x: (x[0 : int(block_size / 2)], x[int(block_size / 2) :])
str_split = lambda x: [x[i : i + block_size] for i in range(0, len(x), block_size)]
xor = lambda x, y: x ^ y


def s(a, b):
    return sa[a], sb[b]


def p(a):
    return a[5] + a[2] + a[3] + a[1] + a[6] + a[0] + a[7] + a[4]


def ks(k):
    return [
        k[i : i + int(block_size)] + k[0 : (i + block_size) - len(k)]
        for i in range(rounds)
    ]


def kx(state, k):
    return [xor(state[i], k[i]) for i in range(len(state))]


def en(e):
    encrypted = []
    for i in e:
        a, b = bin_split(to_bin(ord(i)))
        sa, sb = s(to_int(a), to_int(b))
        pe = p(
            bin_join((to_bin(sa, int(block_size / 2)), to_bin(sb, int(block_size / 2))))
        )
        encrypted.append(to_int(pe))
    return encrypted


def r(p, k):
    keys = ks(k)
    state = str_split(p)
    for b in range(len(state)):
        for i in range(rounds):
            rk = kx(to_ord(state[b]), keys[i])
            state[b] = to_chr(en(to_chr(rk)))
    return [ord(e) for es in state for e in es]


encrypted_flag = [
    190,
    245,
    36,
    15,
    132,
    103,
    116,
    14,
    59,
    38,
    28,
    203,
    158,
    245,
    222,
    157,
    36,
    100,
    240,
    206,
    36,
    205,
    51,
    206,
    90,
    212,
    222,
    245,
    83,
    14,
    222,
    206,
    163,
    38,
    59,
    157,
    83,
    203,
    28,
    27,
]

flag = "247"

key = []
for i in range(256):
    for j in range(256):
        key = [i, j] * 4
        encrypted_test_flag = r(flag, key)
        if (
            encrypted_test_flag[0] == encrypted_flag[0]
            and encrypted_test_flag[1] == encrypted_flag[1]
            and encrypted_test_flag[2] == encrypted_flag[2]
        ):
            key = [i, j] * 4
            break
    else:
        continue

    break

idx = 3
while flag[-1] != "}":
    for char in printable:
        test_flag = flag + char
        encrypted_test_flag = r(test_flag, key)
        if encrypted_test_flag[idx] == encrypted_flag[idx]:
            flag = test_flag
            idx += 1
            break

print(flag)
