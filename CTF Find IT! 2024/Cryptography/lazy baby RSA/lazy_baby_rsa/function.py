import base64
from math import ceil, floor, sqrt


def convert(text, a):
    for _ in range(a):
        text = base64.b64encode(text.encode()).decode()
    return text


def modify(n, p):
    n_str = str(n)
    list = []

    for digit_char in n_str:
        digit = int(digit_char)
        modified_digit = (digit**p) % 10
        list.append(str(modified_digit))

    modified_number = "".join(list)
    result = int(modified_number)

    return result


def modify_digit(n, rules):
    n_str = str(n)
    nums = []

    for char in n_str:
        digit = int(char)

        if digit in rules:
            modified_digit = rules[digit](digit)
        else:
            modified_digit = digit

        nums.append(str(modified_digit))

    num = "".join(nums)
    result = int(num)

    return result


def rule1(n):
    return pow(n, n + (n**0))


def rule2(n):
    return pow(n, n * (n - 1), n ** (n - 1) + n**0)


def rule3(n):
    return pow(n * (n + 1), int(n * sqrt(n) + 1), int(n * sqrt(n) - 1))


def rule4(n):
    return pow(ceil(sqrt(n)), 1, n)


def rule5(n):
    return pow(ceil(3.14 * n * (n + 1)), 1, (ceil(sqrt(n))) * (ceil(sqrt(n))) + n**0)


def rule6(n):
    return ceil(sqrt(n)) + floor(sqrt(n))


def rule7(n):
    return n - 1


def rule8(n):
    return pow((n - (n**0 + 1)), int(sqrt(n) - 1), int(sqrt(n) + ceil(sqrt(sqrt(n)))))


rules = {
    2: rule1,
    3: rule2,
    4: rule3,
    5: rule4,
    6: rule5,
    7: rule6,
    8: rule7,
    9: rule8,
}
