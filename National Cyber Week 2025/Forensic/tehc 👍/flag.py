_T7 = 716267
_a1 = "e7ac7a29"
_b2 = "dd993a2e"
_c3 = "e8aa700e"
_d4 = "d5b03705"
_e5 = "ef9b2005"
_f6 = "dd9e3513"
_g7 = "ec952a28"
_h8 = "d9a125f6"
_i9 = "dc9c3a37"
_j0 = "05b33a12"
_k1 = "ee9b2005"
_l2 = "07a62938"
_m3 = "09b12b2a"
_n4 = "e99150d9"

_H0 = list(
    _a1 + _b2 + _c3 + _d4 + _e5 + _f6 + _g7 + _h8 + _i9 + _j0 + _k1 + _l2 + _m3 + _n4
)


def _r(x, n):
    n = n & 31
    return ((x << n) | ((x & 4294967295) >> (32 - n))) & 4294967295


def _n(b):
    return ((b << 4) & 240) | ((b >> 4) & 15)


def _p(b4):
    return bytes([b4[1], b4[3], b4[0], b4[2]])


def _u(hs, tid):
    k = tid & 4294967295
    c = (2654435769 * k) & 4294967295
    d = [int(x) for x in str(tid)]
    z = bytes.fromhex("".join(hs))
    q = [z[i : i + 4] for i in range(0, len(z), 4)]
    w = []

    while q:
        w.append(q.pop())

    o = []
    for ci, ch in enumerate(w):
        sb = bytearray(4)
        for i in range(4):
            sb[i] = (ch[i] ^ d[(ci * 4 + i) % len(d)]) & 255
        v = int.from_bytes(bytes(sb), "big")
        v = (v ^ c) & 4294967295
        v ^= k
        v = _r(v, 4)
        b4 = v.to_bytes(4, "big")
        b4 = _p(b4)
        b4 = bytes(_n(b) for b in b4)
        for ch2 in b4.decode("ascii"):
            o.append(ch2)

    return "".join(reversed(o))


print(_u(_H0, _T7))
