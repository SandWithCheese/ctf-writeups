# Intercepted from Alice: {"p": "0xde26ab651b92a129", "g": "0x2",
# "A": "0x62fd0e4e04b9bdce"}
# Intercepted from Bob: {"B": "0x6c2cd2a2085b5f88"}
# Intercepted from Alice: {"iv": "f7c0ef4a1403d4dd064c55f4532b9ad3",
# "encrypted_flag": "c6c5b6fa8911267cc7d78f16133974c73dc5f75cdf87744b97c7f43ed6890c67"}

from math import log, floor

p = 0xDE26AB651B92A129
g = 0x2

A = 0x62FD0E4E04B9BDCE
B = 0x6C2CD2A2085B5F88

# g^x = A
# x = glogA

x = floor(log(A, g))
# print(pow(2, x))
# print(A)

for i in range(x, p):
    if pow(g, i, p) == A:
        print(i)
        break
