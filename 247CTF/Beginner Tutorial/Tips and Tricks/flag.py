import pwn

conn = pwn.remote("8ceb966abc94c4f5.247ctf.com", 50283)

conn.recvline()

for i in range(500):
    conn.recvline()
    p = conn.recvline().decode().split()
    a = int(p[5])
    b = int(p[7][:-1])
    print(i + 1)
    conn.sendline(f"{a + b}\r\n".encode())

conn.recvline()
print(conn.recvline().decode().strip())
