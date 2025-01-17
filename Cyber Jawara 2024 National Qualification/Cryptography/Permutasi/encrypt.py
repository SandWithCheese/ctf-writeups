import random


def encrypt(msg, key):
    keylen = len(key)

    k = list(range(keylen))
    for i in range(keylen):
        for j in range(i + 1, keylen):
            if key[i] > key[j]:
                key[i], key[j] = key[j], key[i]
                k[i], k[j] = k[j], k[i]

    print(k)

    m = ""
    for i in k:
        j = i
        while j < len(msg):
            m += msg[j]
            j += keylen

    return m


k = random.sample(range(256), 10)

m = input("Enter a message: ")
m = encrypt(m, k)

print("Encrypted message:", m)
