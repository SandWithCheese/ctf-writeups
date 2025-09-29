#!/usr/bin/env python3
# minimal TCP (netcat-like) solver: connect, send HELLO, read banner, print flags

import sys, re, socket, time

FLAG_RE = re.compile(r"(FLAG\{[^}]+\}|CTF\{[^}]+\})")
TIMEOUT = 3

def eprint(*a, **k): print(*a, file=sys.stderr, **k)
def extract(s): return [m.group(0) for m in FLAG_RE.finditer(s or "")]

def try_socket(host, port):
    out=[]
    try:
        s = socket.create_connection((host,int(port)), timeout=TIMEOUT)
        s.settimeout(TIMEOUT)
        try:
            # read initial banner
            try:
                banner = s.recv(2048).decode(errors="ignore")
                out += extract(banner)
            except Exception:
                pass
            # send a simple probe
            try:
                s.sendall(b"HELLO\n")
                time.sleep(0.1)
                data = s.recv(4096).decode(errors="ignore")
                out += extract(data)
            except Exception as e:
                eprint("sock probe error", repr(e))
        finally:
            s.close()
    except Exception as e:
        eprint("sock connect", host, port, repr(e))
    if out:
        eprint("sock", host, port, "found")
    return out

def main():
    if len(sys.argv) < 3:
        eprint("usage: solver_netcat.py <host> <port>"); sys.exit(2)
    host, port = sys.argv[1], sys.argv[2]
    flags = try_socket(host, port)
    seen=set()
    for f in flags:
        if f not in seen:
            seen.add(f)
            print(f)
    sys.exit(0)

if __name__=="__main__":
    main()
