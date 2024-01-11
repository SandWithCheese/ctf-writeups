import string
from pprint import pprint

LOWERCASE_OFFSET = ord("a")
ALPHABET = string.ascii_lowercase[:16]
HEX_ALPHABET = "abcdef0123456789"

possible_index = {}
for k in ALPHABET:
    for c in HEX_ALPHABET:
        t1 = ord(c) - LOWERCASE_OFFSET
        t2 = ord(k) - LOWERCASE_OFFSET
        index = ALPHABET[(t1 + t2) % len(ALPHABET)]

        if index not in possible_index:
            possible_index[index] = []
        possible_index[index].append((k, c))


pprint(possible_index)

enc_flag = "bkglibgkhghkijphhhejggikgjkbhefgpienefjdioghhchffhmmhhbjgclpjfkp"
# enc_flag = "bkgl"

# for char in enc_flag:
#     print(possible_index[char])

# possible_keys = []
# for char in enc_flag:
#     pair = possible_index[char]
#     keys, c = list(zip(*pair))
#     possible_keys.append(list(set(keys)))

# a, b, c, d = possible_keys
# for i in a:
#     for j in b:
#         for k in c:
#             print(i + j + k)
