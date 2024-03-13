import requests

url = "https://aes.cryptohack.org/symmetry"

s = requests.Session()

res = bytes.fromhex(s.get(url=f"{url}/encrypt_flag").json()["ciphertext"])

iv, flag = res[:16].hex(), res[16:].hex()

res = s.get(url=f"{url}/encrypt/{flag}/{iv}").json()["ciphertext"]
print(bytes.fromhex(res).decode())
