import math
import hashlib
import sys
from tqdm import tqdm
import functools
from gmpy2 import mpz

ITERS = int(2e7)
VERIF_KEY = "96cc5f3b460732b442814fd33cf8537c"
ENCRYPTED_FLAG = bytes.fromhex(
    "42cbbce1487b443de1acf4834baed794f4bbd0dfe2d6046e248ff7962b"
)


# This will overflow the stack, it will need to be significantly optimized in order to get the answer :)
@functools.cache
def m_func(n):
    return (
        1612 * (mpz(-21) ** int(n))
        + 981920 * (mpz(12) ** int(n))
        - 1082829 * (mpz(13) ** int(n))
        + 141933 * (mpz(17) ** int(n))
    ) // 42636


# m(4) = 55692 - 9549*2 + 301*3 + 21*4


# Decrypt the flag
def decrypt_flag(sol):
    sol = sol % (10**10000)
    sol = str(sol)
    sol_md5 = hashlib.md5(sol.encode()).hexdigest()

    if sol_md5 != VERIF_KEY:
        print("Incorrect solution")
        sys.exit(1)

    key = hashlib.sha256(sol.encode()).digest()
    flag = bytearray([char ^ key[i] for i, char in enumerate(ENCRYPTED_FLAG)]).decode()

    print(flag)


if __name__ == "__main__":
    sol = m_func(ITERS)
    decrypt_flag(sol)
