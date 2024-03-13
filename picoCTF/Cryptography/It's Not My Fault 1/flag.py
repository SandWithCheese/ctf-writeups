import pwn
import hashlib

host, port = "mercury.picoctf.net", 27379

conn = pwn.remote(host, port)

line = conn.recvline().decode().split()

startswith = line[6].strip('"')
endswith = line[-1]

serching = True
i = 0
ans = b""
while serching:
    tmp = startswith.encode() + hex(i)[2:].encode()
    i = i + 1
    md5_hash = hashlib.md5(tmp).hexdigest()
    if md5_hash.endswith(endswith):
        ans = tmp
        break

conn.sendline(ans)

conn.interactive()
