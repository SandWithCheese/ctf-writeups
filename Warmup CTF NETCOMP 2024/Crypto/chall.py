#!/usr/bin/env python3

from Crypto.Util.number import bytes_to_long

flag = "<REDACTED>".encode()

p = 1089915817272225657529571741047
q = 1230438593754451648545439211911
e = 65537
n = p * q
c = bytes_to_long(flag)

encrypt = pow(c, e, n)
print(encrypt)

"""
output: 432129069781466954970115267255448126809679346680737712720914
"""
