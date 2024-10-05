from Crypto.Util.number import getPrime, bytes_to_long

while True:
    try:
        p = getPrime(512)
        q = getPrime(512)
        n = []

        for i in range(16):
            q = p
            p = getPrime(512)
            n.append(p * q)

        m = bytes_to_long(b"COMPFEST16{SECRET}")
        e = 65537
        c = pow(m, e, n[0])

        for i in range(1, 16):
            assert c < n[i], i
            c = pow(c, e, n[i])

        with open("chall2_mem.txt", "w") as f:
            f.write(f"n = {n}\n")
            f.write(f"e = {e}\n")
            f.write(f"c = {c}\n")

        break

    except AssertionError as e:
        print(f"Assertion error: {e}. Retrying...")

