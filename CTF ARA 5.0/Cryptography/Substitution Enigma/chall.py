import random
from secret import flag

cycle = 5
block_size = 8
s1 = {
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
    15: 5
}
s2 = {
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
    15: 2
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
    return s1[a], s2[b]

def p(a):
    return a[5] + a[2] + a[3] + a[1] + a[6] + a[0] + a[7] + a[4]

def rnd_keys(k):
    return [
        k[i : i + int(block_size)] + k[0 : (i + block_size) - len(k)]
        for i in range(cycle)
    ]

def xkey(state, k):
    return [xor(state[i], k[i]) for i in range(len(state))]

def en(e):
    encrypted = []
    for i in e:
        a, b = bin_split(to_bin(ord(i)))
        s1, s2 = s(to_int(a), to_int(b))
        pe = p(
            bin_join((to_bin(s1, int(block_size / 2)), to_bin(s2, int(block_size / 2))))
        )
        encrypted.append(to_int(pe))
    return encrypted

def run(p, k):
    keys = rnd_keys(k)
    state = str_split(p)
    for b in range(len(state)):
        for i in range(cycle):
            rk = xkey(to_ord(state[b]), keys[i])
            state[b] = to_chr(en(to_chr(rk)))
    return [ord(e) for es in state for e in es]

enc = run(flag, key)
print("Encrypted flag => %s" % enc)
# enc => [8, 167, 8, 118, 243, 40, 84, 118, 208, 133, 241, 141, 136, 170, 225, 118, 201, 117, 121, 218, 208, 218, 201, 40, 70, 133, 68, 133, 208, 214, 113, 189, 12]
