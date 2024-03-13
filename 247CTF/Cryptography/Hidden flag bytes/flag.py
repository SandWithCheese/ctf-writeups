import requests
from string import ascii_letters, digits
from binascii import hexlify
from pwn import xor

chars = ascii_letters + digits + "{}"
chars_hex = []
for char in chars:
    char = hexlify(char.encode())
    chars_hex.append(char.decode())

print(chars_hex)

url = "https://6c731a1136cffdf0.247ctf.com/"
encrypt_url = f"{url}encrypt?plaintext="

s = requests.Session()

flag = s.get(url=encrypt_url).text
print(len(bytes.fromhex(flag)))

payload = "AA" * 16
flag_block = s.get(url=f"{encrypt_url}{payload}").text[32:64]
print(flag_block)
# print(xor(payload, flag_block))
print(xor(b"AA", hexlify("2".encode())))
print(xor(b"AA", hexlify("4".encode())))
print(xor(b"AA", hexlify("7".encode())))
print(xor(b"AA", hexlify("C".encode())))
print(xor(b"AA", hexlify("T".encode())))
print(xor(b"AA", hexlify("F".encode())))
# AA ^ dec(65) = hex(2)

payload = "BB" * 16
print(s.get(url=f"{encrypt_url}{payload}").text[32:64])

print(xor(b"BB", hexlify("2".encode())))
print(xor(b"BB", hexlify("4".encode())))
print(xor(b"BB", hexlify("7".encode())))
print(xor(b"BB", hexlify("C".encode())))
print(xor(b"BB", hexlify("T".encode())))
print(xor(b"BB", hexlify("F".encode())))

# BB ^ dec(f9) = hex(2)
# calon_flag = ""
# for i in range(9, 17):
#     payload = payload*i
#     for char in chars_hex:
