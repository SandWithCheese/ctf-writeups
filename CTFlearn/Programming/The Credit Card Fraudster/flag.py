from itertools import product
from string import digits

credit_card = "543210******1234"


def check(i, char):
    total = 0
    if char.isdigit():
        idx = i % 2
        if idx == 0:
            x = int(char) * 2
            if x > 9:
                x = x // 10 + x % 10
            total += x
        else:
            total += int(char)

    return total


total = 0
for i, char in enumerate(credit_card):
    total += check(i, char)


for i in product(digits, repeat=6):
    new_total = total
    for j, char in enumerate(i):
        new_total += check(j, char)

    if new_total % 10 == 0:
        valid = f"543210{''.join(i)}1234"
        if int(valid) % 123457 == 0:
            print(valid)
            break
