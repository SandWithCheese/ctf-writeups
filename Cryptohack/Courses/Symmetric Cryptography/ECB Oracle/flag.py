import requests

hex_byte = []
for i in range(256):
    byte = hex(i)[2:]
    if len(byte) == 1:
        byte = "0" + byte
    hex_byte.append(byte)


url = "https://aes.cryptohack.org/ecb_oracle/encrypt/"

s = requests.Session()

i = 0
pad = 15
# flag = ""
flag = "3675316e355f683437335f3363627d"
# while i < 16:
#     pl = "AA" * (8 + i)

#     block = s.get(url=f"{url}/{pl}").json()["ciphertext"]
#     last_block = block[-32:]

#     for byte in hex_byte:
#         payload = byte + flag + hex_byte[pad] * pad
#         brute_block = s.get(url=f"{url}/{payload}").json()["ciphertext"]
#         first_block = brute_block[:32]
#         print(byte)
#         if last_block == first_block:
#             flag = byte + flag
#             break

#     pad -= 1
#     i += 1

#     print(f"Flag: {flag}")

# i = 15
# while i < 25:
#     pl = "AA" * (8 + i)

#     block = s.get(url=f"{url}/{pl}").json()["ciphertext"]
#     second_last_block = block[-64:-32]

#     for byte in hex_byte:
#         payload = byte + flag + hex_byte[pad] * pad
#         brute_block = s.get(url=f"{url}/{payload}").json()["ciphertext"]
#         first_block = brute_block[:32]
#         print(byte)
#         if second_last_block == first_block:
#             flag = byte + flag
#             break

#     pad -= 1
#     i += 1

#     print(f"Flag: {flag}")


flag = "63727970746f7b70336e3675316e355f683437335f3363627d"

print(bytes.fromhex(flag).decode())
