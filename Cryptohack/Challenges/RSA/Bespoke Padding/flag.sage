from pwn import *
import json
import z3
from Crypto.Util.number import long_to_bytes

host, port = "socket.cryptohack.org", "13386"

json_data = b'{"option": "get_flag"}'
e = 11

conn = remote(host, port)
conn.recvline()

conn.sendline(json_data)
res = conn.recvline()
data = json.loads(res)

enc_flag = data["encrypted_flag"]
modulus = data["modulus"]
padding = data["padding"]
a, b = padding

inv_enc_flag = pow(enc_flag, -e, modulus)

i = 1
while True:
    # print("sat")
    x = (modulus * i + 1) // inv_enc_flag
    if enc_flag == pow(x, e, modulus):
        print(f"Found m: {x}")
        break
    i += 1

# s = z3.Solver()
# x = z3.Int("x")
# s.add((x * inv_enc_flag - 1) % modulus == 0)
# s.add(x > 0)

# while s.check() == z3.sat:
#     print("sat")
#     m = s.model()
#     m = m[x].as_long()
#     if enc_flag == pow(m, e, modulus):
#         print(f"Found m: {m}")
#         break
#     s.add(x != m)

# if s.check() == z3.sat:
#     print("sat")
#     m = s.model()
#     m = m[x].as_long()
#     print(m)
#     print(enc_flag == pow(m, e, modulus))

conn.interactive()

# while True:
#     conn = remote(host, port)
#     conn.recvline()

#     conn.sendline(json_data)
#     res = conn.recvline()
#     data = json.loads(res)

#     enc_flag = data["encrypted_flag"]
#     modulus = data["modulus"]
#     padding = data["padding"]
#     a, b = padding

#     inv_enc_flag = pow(enc_flag, -e, modulus)

#     s = z3.Solver()
#     x = z3.Int("x")
#     s.add((x * inv_enc_flag - 1) % modulus == 0)
#     s.add(x > 0)

#     if s.check() == z3.sat:
#         print("sat")
#         m = s.model()
#         m = m[x].as_long()
#         if enc_flag == pow(m, e, modulus):
#             print(f"Found m: {m}")
#             conn.interactive()
#         else:
#             conn.close()
