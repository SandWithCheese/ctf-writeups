import re, sys, struct

data = open("elf.bin", "rb").read()
for m in re.finditer(b"MEI\x0c\x0b\x0a\x0b\x0e", data):
    off = m.start()
    # CArchive has a 8-byte length right after magic (little-endian unsigned long long)
    # Many variants: try to read len and carve; fall back to large slice if crazy.
    try:
        size = struct.unpack_from("<Q", data, off + 8)[0]
        blob = data[off : off + 8 + size] if 0 < size < len(data) else data[off:]
    except Exception:
        blob = data[off:]
    out = f"carved_MEI_{off}.bin"
    print(out)
    open(out, "wb").write(blob)
    print("carved", out, len(blob))
