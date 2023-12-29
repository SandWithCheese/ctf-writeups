# with open("garbage.py", "r") as f:
#     lines = f.readlines()

# bfuck = ""
# for line in lines:
#     if "#" in line:
#         bfuck += line[line.index("#") + 2 :] + "\n"

# print(bfuck)

import string
from random import *


def finalstage(w):
    h = 0
    # w = list(w)
    # w.reverse()
    # w = "".join(g for g in w)
    w = w[::-1]
    # flag = "flag".replace("flag", "galf").replace("galf", "")
    flag = ""
    while h < len(w):
        try:
            flag += w[h + 1] + w[h]
        except:
            flag += w[h]
        h += 2
    print("Final Stage complete")
    return flag


def stage2(b):
    # t = "++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>>++.++++++.-----------.++++++."[
    #     -15 : (7 * 9)
    # ].strip("-")
    t = ""
    for q in range(len(b)):
        t += chr(ord(b[q]) - randint(0, 5))
    print("Stage 2 complete")
    flag = finalstage(t)
    return flag


def stage1(a):
    a = list(a)
    # b = list(string.ascii_lowercase)
    for o in range(len(a)):
        a[o] = chr(ord(a[o]) ^ o)
    z = "".join(x for x in a)
    # for y in range(len(z)):
    #     b[y % len(b)] = chr((ord(z[y]) ^ ord(a[y])) + len(b))
    print("Stage 1 complete")
    flag = stage2(z)
    return flag


def entry(f):
    seed(10)
    # f = list(f)
    # f.reverse()
    # f = "".join(i for i in f)
    f = f[::-1]
    print("Entry complete")
    flag = stage1(f)
    return flag


if __name__ == "__main__":
    decrypted = r"^seqVVh+]>z(jE=%oK![b$\NSu86-8fXd0>dy"

    h = 0
    flag1 = ""
    while h < len(decrypted):
        try:
            flag1 += decrypted[h + 1] + decrypted[h]
        except:
            flag1 += decrypted[h]
        h += 2

    flag1 = flag1[::-1]
    t = flag1

    seed(10)
    b = ""
    for q in range(len(t)):
        b += chr(ord(t[q]) + randint(0, 5))
    # print(b)

    z = list(b)
    for o in range(len(z)):
        z[o] = chr(ord(z[o]) ^ o)
    a = "".join(z)
    print(a[::-1])
    # input = entry(input("Enter Flag: "))
    # flag = open("output.txt", "r").readlines()[0]
    # if input == flag:
    #     print("What... how?")
    #     print("I guess you broke my 'beautiful' code :(")
    # else:
    #     print(input)
    #     print("haha, nope. Try again!")
