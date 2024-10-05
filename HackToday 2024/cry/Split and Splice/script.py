from Crypto.Util.number import bytes_to_long as b2l


def grey_v2(x):
    n = x ^ (x // 2) ^ (x // 4)
    return n


def grey_v3(x):
    n = (2 * x) ^ (x) ^ (x // 2) ^ (x // 4)
    return n


with open("secret.txt", "rb") as file:
    flag = file.read()

fp1 = b2l(flag[: (len(flag) // 2)])
# print(flag[: (len(flag) // 2)])
fp2 = b2l(flag[(len(flag) // 2) :])

n1 = fp1
for _ in range(1000):
    n1 = grey_v2(n1)

n2 = fp2
for _ in range(1000):
    n2 = grey_v3(n2)

# print(n1)
# print()
# print(n2)

print(len(str(n1)))
print()
print(len(str(n2)))
print(len(str(n1) + str(n2)))

# with open("file.txt", "w") as file:
#     # Menulis konten ke file
#     file.write(f"ct={str(n1)+str(n2)}")
