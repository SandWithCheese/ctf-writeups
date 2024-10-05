import requests
from hashlib import sha256, sha512, sha3_256, sha3_512, blake2b, blake2s
from Crypto.Util.number import bytes_to_long, long_to_bytes
from string import ascii_letters, digits
from itertools import product
from tqdm import tqdm

strings = ascii_letters + digits + "{}_"


# BASE_URL = "http://challenges.ctf.compfest.id:9010/"
BASE_URL = "http://127.0.0.1:5000/"

algo_round = [sha256, sha3_256, sha3_512, blake2b, blake2s]

magic_string = b"SkibidiSigmaRizzleDizzleMyNizzleOffTheHizzleShizzleKaiCenat"


def xor_256(a: bytes, b: bytes):
    if len(a) < len(b):
        a = a + b"\x00" * (len(b) - len(a))
    elif len(b) < len(a):
        b = b + b"\x00" * (len(a) - len(b))
    return bytes([x ^ y for x, y in zip(a, b)])


def sigma_round(bytes_to_hash: bytes):
    result = b""
    for i in range(0, len(bytes_to_hash), 4):
        current = bytes_to_hash[i : i + 4]
        current = algo_round[i % len(algo_round)](current).digest()[:2]

        result += current
    return result


def icb_256(bytes_to_hash: bytes):
    if len(bytes_to_hash) < 64:
        bytes_to_hash = sha512(bytes_to_hash).digest()

    temp = sigma_round(bytes_to_hash)
    result = b""
    for i in range(0, len(temp), 32):

        result = xor_256(result, temp[i : i + 32])

    return result


def get_pubkey():
    return requests.get(BASE_URL + "pubkey").json()


def sign_message(message: bytes):
    return requests.get(BASE_URL + "sign", params={"message": message.hex()}).json()


def get_flag(signature: int):
    return requests.get(BASE_URL + "get_flag", params={"signature": signature}).text


pubkey = get_pubkey()
e = int(pubkey["e"])
n = int(pubkey["n"])

# print(n)

# # Sign n
# signed_message = sign_message(long_to_bytes(n))["signature"]
# print(signed_message)

# flag = get_flag(signed_message)
# print(flag)

# magic_hash = sha512(magic_string).digest()
# magic_round = sigma_round(magic_hash)

# collision = b""
# j = 0
# for i in range(0, 64, 4):
#     for s in tqdm(product(strings, repeat=4)):
#         s = "".join(s).encode()
#         payload = collision + s
#         temp_round = sigma_round(payload)

#         if (
#             temp_round[j : j + 2] == magic_round[j : j + 2]
#             and s != magic_string[i : i + 4]
#         ):
#             print(f"Found: {s}")
#             collision += s
#             break
#     j += 2

# signature = sign_message(collision)
# print(signature)
# flag = get_flag(signature["signature"])
# print(flag)

signature = sign_message(magic_string)
print(signature)
flag = get_flag(signature["signature"])
print(flag)
