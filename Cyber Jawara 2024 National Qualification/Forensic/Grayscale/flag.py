from binascii import hexlify, unhexlify

with open("grayscale.gif", "rb") as f:
    gif = f.read()

with open("sus.gif", "rb") as f:
    sus = f.read()


hexed_gif = hexlify(gif).decode()[1562:]
healthy_header = hexlify(sus[:0x320]).decode()

with open("healthy.gif", "wb") as f:
    f.write(unhexlify(healthy_header + hexed_gif))
