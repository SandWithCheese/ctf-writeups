# x = 588


# def is_prime(n: int) -> bool:
#     if n == 1:
#         return False

#     if n % 2 == 0:
#         return False

#     i = 3
#     while i * i <= n:
#         if n % i == 0:
#             return False
#         i += 2
#     return True


# congruences = [588, 665, 216, 113, 642, 4, 836, 114, 851, 492, 819, 237]

# list_of_primes = []
# for i in range(852, 1000):
#     if is_prime(i):
#         list_of_primes.append(i)

# # print(list_of_primes)

# for prime in list_of_primes:
#     for x in range(2, prime):
#         congruence = []
#         for i in range(1, prime):
#             congruence.append(pow(x, i, prime))
#         if congruences in congruence:
#             print(x)
#             print(prime)
#     # print()

# a mod p = 588

prime = [
    853,
    857,
    859,
    863,
    877,
    881,
    883,
    887,
    907,
    911,
    919,
    929,
    937,
    941,
    947,
    953,
    967,
    971,
    977,
    983,
    991,
    997,
]
m = [588, 665, 216, 113, 642, 4, 836, 114, 851, 492, 819, 237]
flag = True
for p in prime:
    for x in range(2, 1000):
        for i in range(len(m) - 1):
            if m[i] * x % p == m[i + 1]:
                flag = True
            else:
                flag = False
                break
        if flag:
            print("crypto{" + str(p) + "," + str(x) + "}")
            break
    if flag:
        break
