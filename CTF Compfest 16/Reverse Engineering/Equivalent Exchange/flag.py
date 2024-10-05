from ctypes import c_int32
from itertools import product


def int32(val):
    return c_int32(val).value


def check1(p: int):
    count = 0
    while p != 0:
        count += 1
        p //= 10

    return 15 < count


def check2(p: int, q: int):
    if q == 0:
        return False

    count_1 = 0
    temp_q = q
    while temp_q != 0:
        count_1 += temp_q & 1
        temp_q >>= 2

    if count_1 < 7:
        return False

    count = 0
    temp_p = p
    while temp_p != 0:
        count += int32(temp_p) + int32(temp_p // 10 << 2) + int32((temp_p // 10)) * -2
        temp_p //= 10

    print(count)

    temp_q = q
    while temp_q != 0:
        count += -(
            int32(temp_q) + int32(temp_q // 10 << 2) + int32((temp_q // 10)) * -2
        )
        temp_q //= 10

    print(count)

    return count == 105


def check3(p: int):
    if p >= 0:
        return False

    count = 0
    temp_p = p
    while temp_p != -1:
        temp = temp_p
        temp_p >>= 1

        temp_counter = 0
        temp_count = count
        while temp_count != 0:
            temp_counter += 1
            temp_count >>= 1

        count = (count | (temp & 1)) << (temp_counter & 63)

    # print(bin(p))
    # print(bin(count))

    return bin(abs(p)) == (bin(abs(count)))


def check4(p: int, q: int):
    if q & 1 == 0 or q == 1:
        return False

    temp_p = p
    if q <= p:
        temp_p = q

    while temp_p != 0 and (p % temp_p != 0 or q % temp_p != 0):
        temp_p -= 1

    return temp_p == 1


# 1010101010101 >> 2 = 0010101010101


# print(check1(1_000_000_000_000_000))
# print(check2(1_000_000_000_000_000, 1_499_999_999_999_866))
# print(check2(1_000_000_000_000_000, 5461))
print(check2(1_000_000_000_000_000, 999_999_999_999_952))
# print(check3(-15060318633198616577))
# print(check4(15060318633198616577, 5))

# i = pow(2, 63) + 1
# i = int("1101000100000001000000000000000100000000000000000000000000000001", 2)
# print(i)
# print(i)
# print(check3(-i))
