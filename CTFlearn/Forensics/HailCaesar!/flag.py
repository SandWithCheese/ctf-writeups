enc = "2m{y!\"%w2'z{&o2UfX~ws%!._s+{ (&@Vwu{ (&@_w%{v{(&0"


def printable_caesar(s, shift):
    return "".join([chr((ord(c) + shift - 32) % 95 + 32) for c in s])


print(printable_caesar(enc, -18))
