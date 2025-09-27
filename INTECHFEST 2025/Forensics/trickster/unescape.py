import sys, json, re, pathlib

buf = bytearray()
txt = sys.stdin.read()


# sysdig may output JSON per-line or an array; handle both
def feed(ev):
    for a in ev.get("evt", {}).get("args", []):
        print(a)
        if a.get("name") == "data":
            s = a.get("value", "")

            # convert \xNN escapes to raw bytes
            def repl(m):
                return bytes([int(m.group(1), 16)]).decode("latin1")

            out = re.sub(r"\\x([0-9a-fA-F]{2})", repl, s).encode("latin1")
            buf.extend(out)


try:
    obj = json.loads(txt)
    if isinstance(obj, list):
        for ev in obj:
            feed(ev)
    else:
        feed(obj)
except Exception:
    for line in txt.splitlines():
        try:
            feed(json.loads(line))
        except:
            pass
pathlib.Path("flag.txt.enc.000000").write_bytes(buf)
print(f"wrote {len(buf)} bytes to flag.txt.enc.000000", file=sys.stderr)
