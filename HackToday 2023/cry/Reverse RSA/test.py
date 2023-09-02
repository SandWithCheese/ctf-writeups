from sympy import integer_nthroot

c = 62324783949134119159408816513334912534343517300880137691662780895409992760262021
n = 1280678415822214057864524798453297819181910621573945477544758171055968245116423923
p = 1899107986527483535344517113948531328331
q = 674357869540600933870145899564746495319033
e = 3

phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)

print(f"{phi = }")
print(f"{d = }")

hint1 = pow(d, e, n)
# h1 = d^e mod n
# d^e - h1 = kn
# d^e = h1 + kn
hint2 = pow(phi, e, n)

print(f"{hint1 = }")
print(f"{hint2 = }")

# print(pow())
i = 0
while True:
    tmp = hint1 + i * n
    root, isroot = integer_nthroot(tmp, e)
    if isroot:
        print(root)
        break
