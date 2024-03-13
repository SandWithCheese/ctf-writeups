import string
from itertools import permutations

ALPHABET = string.ascii_lowercase[:16]


def shift(c, k):
    t1 = ord(c) - 97  # 0-15
    t2 = ord(k) - 97  # 0-15
    return ALPHABET[(t1 + t2) % 16]


def unshift(c, k):
    # idx = (t1 + t2) % 16
    # t1+t2-idx = 16k
    # t1 + t2 = 16k + idx
    idx = ALPHABET.index(c)
    return


flag = "bkglibgkhghkijphhhejggikgjkbhefgpienefjdioghhchffhmmhhbjgclpjfkp"

keys = list(permutations(ALPHABET, 2))
# print(flag)
print(keys)
