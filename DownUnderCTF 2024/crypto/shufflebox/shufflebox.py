import random

# PERM = list(range(16))
# random.shuffle(PERM)

PERM = [9, 10, 0, 8, 11, 13, 3, 6, 15, 5, 14, 7, 4, 2, 12, 1]


def apply_perm(s):
    assert len(s) == 16
    return "".join(s[PERM[p]] for p in range(16))


def rev_perm(s):
    assert len(s) == 16
    return "".join(s[PERM.index(p)] for p in range(16))


# for line in open(0):
# 	line = line.strip()
# 	print(line, '->', apply_perm(line))

print(
    "aaaabbbbccccdddd ->",
    apply_perm("aaaabbbbccccdddd"),
    apply_perm("aaaabbbbccccdddd") == "ccaccdabdbdbbada",
)

print(
    "abcdabcdabcdabcd ->",
    apply_perm("abcdabcdabcdabcd"),
    apply_perm("abcdabcdabcdabcd") == "bcaadbdcdbcdacab",
)

# Reverse
print("owuwspdgrtejiiud ->", rev_perm("owuwspdgrtejiiud"))
