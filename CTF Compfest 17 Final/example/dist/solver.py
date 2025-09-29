#!/usr/bin/env python3
# minimal HTTP solver: try GET / and /flag, print flags to stdout

import sys, re, http.client

FLAG_RE = re.compile(r"(FLAG\{[^}]+\}|CTF\{[^}]+\})")
TIMEOUT = 3

def eprint(*a, **k): print(*a, file=sys.stderr, **k)
def extract(s): return [m.group(0) for m in FLAG_RE.finditer(s or "")]

def try_http(host, port):
    for path in ("/", "/flag"):
        try:
            conn = http.client.HTTPConnection(host, port, timeout=TIMEOUT)
            conn.request("GET", path, headers={"User-Agent":"solver"})
            r = conn.getresponse()
            body = r.read().decode(errors="ignore")
            conn.close()
            flags = extract(body)
            if flags:
                eprint("http", host, port, path, "found")
                return flags
        except Exception as e:
            eprint("http", host, port, path, repr(e))
    return []

def main():
    if len(sys.argv) < 3:
        eprint("usage: solver_http.py <host> <port>"); sys.exit(2)
    host, port = sys.argv[1], sys.argv[2]
    flags = try_http(host, port)
    # dedupe preserving order
    seen=set()
    for f in flags:
        if f not in seen:
            seen.add(f)
            print(f)
    sys.exit(0)

if __name__=="__main__":
    main()
