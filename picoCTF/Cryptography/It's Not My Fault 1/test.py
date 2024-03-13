import hashlib
from string import digits
from itertools import combinations


test_str = "86325"

combinations = list(combinations(digits, 6))

endswith = "f70de5"

# for combination in combinations:
#     temp = test_str + "".join(combination)
#     test = hashlib.md5(temp.encode()).hexdigest()
#     print(test)
#     if test[-6:] == endswith:
#         print(temp)
#         break

serching = True
i = 0
ans = b""
while serching:
    tmp = test_str.encode() + hex(i)[2:].encode()
    i = i + 1
    md5_hash = hashlib.md5(tmp).hexdigest()
    if md5_hash.endswith(endswith):
        ans = tmp
        break

