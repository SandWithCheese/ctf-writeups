from sympy.ntheory.modular import crt

with open("output.txt", "r") as f:
    isi = f.read()

palette = ".=w-o^*"
m = [2, 3, 5, 7]

block = ""
v = []
for i in isi:
    if i != " " and i != "\n":
        v.append(palette.index(i))

    if len(v) == 4:
        print(chr(crt(m, v)[0]), end="")
        v = []
