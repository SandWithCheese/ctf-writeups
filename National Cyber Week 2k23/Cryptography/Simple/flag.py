from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import *

# from string import hexdigits

hexdigits = "0123456789abcdef"

host, port = "103.145.226.206", 1945

conn = remote(host, port)

enckey = conn.recvline().split()[2].strip()
enccode = (
    conn.recvline()
    .split()[2]
    .strip()[2:-1]
    .decode("unicode_escape")
    .encode("raw_unicode_escape")
)
iv2 = (
    conn.recvline()
    .split()[2]
    .strip()[2:-1]
    .decode("unicode_escape")
    .encode("raw_unicode_escape")
)

found = False

print(f"Enckey: {enckey}")
print(f"Enccode: {enccode}")
print(f"iv2: {iv2}")


key = ""
while not found:
    for i in hexdigits:
        for j in hexdigits:
            conn.sendline(b"1")
            conn.recvuntil(b"pesan: ")
            payload = i + j
            conn.sendline(key.encode() + payload.encode())
            print(f"Payload: {key + payload}")
            ciphertext = conn.recvline().split()[2].strip()
            if enckey.startswith(ciphertext):
                key += payload
                print(ciphertext)
                print(key)

            if len(key) == len(enckey):
                found = True

print(f"Key: {key}")
print(f"Enckey: {enckey}")
print(f"Enccode: {enccode}")
print(f"iv2: {iv2}")

plainkey = bytes.fromhex(key)[:-16]

flag = b""
for i in range(256):
    for j in range(256):
        key = plainkey + (chr(i).encode() + chr(j).encode()) * 8
        if len(key) == 32:
            cipher = AES.new(key, AES.MODE_CBC, iv2)
            decrypt = cipher.decrypt(pad(enccode, 16))
            if b"Very" in decrypt:
                flag = decrypt
                break

print(flag)
conn.sendline(b"2")
conn.recvuntil(b"kode: ")
conn.sendline(flag)

conn.interactive()
