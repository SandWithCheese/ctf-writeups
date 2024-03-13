import pwn

conn = pwn.remote("ctf-gemastik.ub.ac.id", 10_001)

conn.recvuntil(b"values:\n")

# n = z1 * z2

# hidden_val = z1 * z2 * z3 + rand_1 = n * z3 + rand_1

# hint_1 = (z3**8) * z2 + 4919 * z2 * (z1**2) + rand_2
# hint_1 = z2 * (z3**8 + 4919 * (z1**2)) + rand_2

# hint_2 = pow(hidden_val, 4 * modd, modd)
# h^4m % m = hint_2 -> h^4m - hint_2 = km
# h^m = 4akar(hint_2 + km)

e = int(conn.recvline().decode().strip()[4:])
c = int(conn.recvline().decode().strip()[4:])
n = int(conn.recvline().decode().strip()[4:])
modd = int(conn.recvline().decode().strip()[7:])
hint_1 = int(conn.recvline().decode().strip()[9:])
hint_2 = int(conn.recvline().decode().strip()[9:])

print(f"{n=}")
print(f"{modd=}")
print(f"{hint_2=}")
# print(secret)
conn.interactive()
