from pwn import *

host, port = "ctf.hackucf.org", 10101

conn = remote(host, port)

conn.recvline()
conn.recvline()

count = 0
for i in range(55):
    value = conn.recvline()
    value = value.strip().split()[1]
    # print(value)
    conn.recvuntil(b"Repeat: ")
    conn.sendline(value)
    count += 1
    print(count)



conn.interactive()