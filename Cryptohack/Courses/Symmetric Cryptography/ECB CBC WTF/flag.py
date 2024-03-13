import requests
from Crypto.Util.number import bytes_to_long, long_to_bytes

url = "https://aes.cryptohack.org/ecbcbcwtf"

s = requests.Session()

res = s.get(url=f"{url}/encrypt_flag").json()["ciphertext"]

res = bytes.fromhex(res)

iv = res[:16]
block_1 = res[16:32]
block_2 = res[32:]


def decrypt(byte):
    res = s.get(url=f"{url}/decrypt/{byte.hex()}").json()["plaintext"]
    return bytes.fromhex(res)


def xor(a, b):
    return long_to_bytes(bytes_to_long(a) ^ bytes_to_long(b))


decrypt1 = xor(decrypt(block_1), iv)
decrypt2 = xor(decrypt(block_2), block_1)

flag = decrypt1 + decrypt2
print(flag.decode())
