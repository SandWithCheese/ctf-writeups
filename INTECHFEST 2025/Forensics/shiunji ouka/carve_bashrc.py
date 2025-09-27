import re, sys

path = "shiunji-ouka.ad1"
off = int(sys.argv[1])
with open(path, "rb") as f:
    f.seek(off)
    chunk = f.read(1024 * 1024)  # scan next 1 MiB
m = re.search(b"\x78[\x9c\xda]", chunk)
print(off + m.start() if m else -1)
# PY $OFF_LABEL

# OFF_ZLIB=<RESULT>
# dd if=shiunji-ouka.ad1 of=bashrc_zlib.bin bs=1 skip=$OFF_ZLIB count=$((128*1024)) status=none
# python3 - <<'PY'
# import zlib, sys

# d = open("bashrc_zlib.bin", "rb").read()
# for w in (15, -15):
#     try:
#         out = zlib.decompress(d, w)
#         open(".bashrc.recovered", "wb").write(out)
#         print("DECOMP_OK wbits", w, "-> .bashrc.recovered", len(out))
#         break
#     except Exception as e:
#         pass
