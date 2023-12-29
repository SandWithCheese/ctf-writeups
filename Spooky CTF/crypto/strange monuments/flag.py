from math import sqrt


def f(x):
    return (pow(x, 3) + 7586 * x + 9001) % 46181


# print(f(20305) == pow(32781, 2, 46181))
x = 20305
y = 32781
count = 0
while x != 39234:
    i = 1
    fx = f(y)
    print(f"{fx = }")
    while True:
        # print(pow(i, 2, 46181))
        if pow(i, 2, 46181) == fx:
            count += 1
            break
        i += 1
    print(i)
    y = i
