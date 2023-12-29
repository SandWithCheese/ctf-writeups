from pwn import xor


def arg122(arg432, arg423):
    arg433 = arg423
    i = 0
    if len(arg433) < len(arg432):
        arg433 = arg433 + arg423[i]
        # print(arg433)
        i = (i + 1) % len(arg423)
        if not len(arg433) < len(arg432):
            return "".join(
                (lambda x: [chr(ord(arg422) ^ ord(arg442)) for arg422, arg442 in x])(
                    zip(arg432, arg433)
                )
            )


with open("flag.txt.enc", "rb") as f:
    enc = f.read()
    print(xor(enc, "ular_sanca"))
