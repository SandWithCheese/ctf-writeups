import requests
from Crypto.Util.number import long_to_bytes, bytes_to_long

url = "https://aes.cryptohack.org/flipping_cookie"

s = requests.Session()

res = s.get(url=f"{url}/get_cookie").json()["cookie"]

res = bytes.fromhex(res)

# print(len(res))
iv = res[:16]
block_1 = res[16:32]
block_2 = res[32:]


def xor(a, b):
    return long_to_bytes(bytes_to_long(a) ^ bytes_to_long(b))


origin = b"admin=False;expi"
goal = b"admin=True;\x05\x05\x05\x05\x05"

new_iv = xor(xor(origin, goal), iv)

flag = s.get(url=f"{url}/check_admin/{block_1.hex()}/{new_iv.hex()}").json()["flag"]
print(flag)
