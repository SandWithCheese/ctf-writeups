# Source Generated with Decompyle++
# File: chall.pyc (Python 3.10)

import sys as S
import re as R

# import flag
from transformers import AutoTokenizer as A

flag = "TechnoFair11{this_is_a_fake_flag}"

T = A.from_pretrained("Xenova/gpt-4")
Tkn = T.tokenize(flag)
Tid = T.convert_tokens_to_ids(Tkn)


def E(n, k="secret-key", w="Technofair"):
    w_o = sum(ord(c) for c in w)
    print(f"w_o: {w_o}")
    k_o = [ord(c) for c in k]
    print(f"k_o: {k_o}")
    k_l = len(k_o)
    print(f"k_l: {k_l}")
    Ecd = [(x ^ k_o[i % k_l]) * w_o for i, x in enumerate(n)]
    return Ecd


def D(n, k="secret-key", w="Technofair"):
    w_o = sum(ord(c) for c in w)
    k_o = [ord(c) for c in k]
    k_l = len(k_o)
    Dcd = [((x // w_o) ^ k_o[i % k_l]) for i, x in enumerate(n)]
    return Dcd


print(Tid)
print(Tkn)

# Ecd = E(Tid, "secret-key")
Ecd = E(Tid)
print(Ecd)

# Dcd = D(E
Dcd = D(Ecd)
print(Dcd)
print(T.convert_ids_to_tokens(Dcd))
