import zlib, sys

d = open("bashrc_zlib.bin", "rb").read()
for w in (15, -15):
    try:
        out = zlib.decompress(d, w)
        open(".bashrc.recovered", "wb").write(out)
        print("DECOMP_OK wbits", w, "-> .bashrc.recovered", len(out))
        break
    except Exception as e:
        pass
