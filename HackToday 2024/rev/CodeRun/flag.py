apaini = [15125, 25570, 8745, 4148, 467, 4148, 15125, 467]
apaan = 34393
apeni = 3217


valueApainiMap = {}
for i in range(10):
    value = (ord(str(i)) + 7) * 99
    res = 1
    apeni2 = apeni
    while apeni2 > 0:
        if apeni2 & 1 == 1:
            res = (res * value) % apaan
        apeni2 >>= 1
        value = (value * value) % apaan

    if res in apaini:
        valueApainiMap[res] = i

x = ""
for i in apaini:
    x += str(valueApainiMap[i])


x = list(x)
for i in range(len(x) - 1, -1, -1):
    j = ((i * 9) + 9) % len(x)
    temp = x[i]
    x[i] = x[j]
    x[j] = temp

print("".join(x))
