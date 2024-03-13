from primefac import primefac

p = 28151
g = 2

s = p - 1

tests = list(set(primefac(s)))

while g < p:
    H = []
    for test in tests:
        root = pow(g, (p - 1) // test, p)
        if root != 1:
            H.append(root)
        else:
            break
    if len(H) == len(tests):
        print(g)
        break
    g += 1
