# i = 0
# # print(i + ((i - i // 7 >> 1) + i // 7 >> 2) * -7)
# while True:
#     eq = i + ((i - i // 7 >> 1) + i // 7 >> 2) * -7
#     if i % 5 == 1 and eq == 3 and i % 109 == 55 and i % 3 == 2:
#         print(i)
#         break
#     i += 2

# i = 10000000000000000000
# jawab = 0
# while i != 0:
#     jawab = jawab + (i & 1)
#     i = i >> 1
# print(jawab)

# local_c0 = 1000
# while (local_c0 & 1) == 0 or (local_c0 == 1) and 1000 <= local_c0 <= 9999:
#     local_c0 += 1

# print(local_c0)

import math


def number_of_digits(n):
    return int(math.log10(n)) + 1


def sum_of_digits(n):
    r = 0
    while n:
        r, n = r + n % 10, n // 10
    return r


# Syarat bear
# bear & 1 == 0 (bear genap)
# bear % 3 == 2
# bear % 5 == 1
# bear + ((bear - bear / 7 >> 1) + bear / 7 >> 2) * -7 == 3
# bear % 109 == 55


def isBear(n):
    return (
        n & 1 == 0
        and n % 3 == 2
        and n % 5 == 1
        and n + ((n - n // 7 >> 1) + n // 7 >> 2) * -7 == 3
        and n % 109 == 55
    )


# Syarat volcano
#   jawab = 0;
#   for (i = param_1; i != 0; i = i >> 1) {
#     jawab = jawab + ((uint)i & 1);
#   }
#   if (jawab < 0x11) {
#     uVar1 = 0;
#   }
#   else if (jawab < 0x1b) {
#     uVar1 = 1;
#   }
#   else {
#     uVar1 = 0;
#   }
#   return uVar1;


def isVolcano(n):
    val = 0
    while n != 0:
        val += n & 1
        n = n >> 1

    return 17 < val < 27


def isValid(n):
    return n & 1 != 0 and n != 1


# Syarat terakhir
#   return_variable = 1;
#   extra = param_1 % param_3;
#   for (i = param_2; i != 0; i = i >> 1) {
#     if ((i & 1) != 0) {
#       return_variable = (return_variable * extra) % param_3;
#     }
#     extra = (extra * extra) % param_3;
#   }
#   return return_variable;


def syaratTerakhir(param_1, param_2, param_3):
    hasil = 1
    extra = param_1 % param_3
    while param_2 != 0:
        if param_2 & 1 != 0:
            hasil = (hasil * extra) % param_3
        extra = (extra * extra) % param_3
        param_2 = param_2 >> 1

    return hasil


b8 = 4919

bear = 1
# print(isBear(18476))
while True:
    # print(bear)
    # if bear > 18500:
    #     break
    if isBear(bear):
        print("Bear done")
        volcano = 1
        while True:
            if (
                isVolcano(volcano)
                and number_of_digits(bear) == number_of_digits(volcano)
                and sum_of_digits(bear) == sum_of_digits(volcano)
            ):
                print("Volcano done")
                c0 = 1
                while True:
                    if isValid(c0):
                        print("Valid")
                        if syaratTerakhir(b8, volcano, c0) == syaratTerakhir(
                            b8, bear, c0
                        ):
                            print(bear)
                            print(volcano)
                            print(c0)
                            quit()
                    c0 += 2
            volcano += 1

            if number_of_digits(volcano) > number_of_digits(bear):
                break
    bear += 1
