#!/usr/bin/env python3
import subprocess
import sys
import base64
from pathlib import Path
from typing import List

PCAP_DEFAULT = "svanm_2025.pcapng"
KEY_HEX = "79eeb31d16154cc17b58b13fb04fd670"  # your only-PE key


def run(cmd: List[str]) -> str:
    return subprocess.check_output(cmd, text=True, errors="ignore")


def get_api_streams(pcap_path: str) -> List[int]:
    cmd = [
        "tshark",
        "-r",
        pcap_path,
        "-Y",
        'ip.addr==192.168.89.133 && http.host=="update.rnicrosoft.com" && http.request.uri=="/api/version"',
        "-T",
        "fields",
        "-e",
        "tcp.stream",
    ]
    out = run(cmd)
    return sorted({int(x) for x in out.split() if x.strip().isdigit()})


def get_stream_ascii(pcap_path: str, stream_id: int) -> str:
    cmd = [
        "tshark",
        "-r",
        pcap_path,
        "-qz",
        f"follow,tcp,ascii,{stream_id}",
    ]
    return run(cmd)


def rc4_ks(key: bytes):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) & 0xFF
        S[i], S[j] = S[j], S[i]
    i = j = 0
    while True:
        i = (i + 1) & 0xFF
        j = (j + S[i]) & 0xFF
        S[i], S[j] = S[j], S[i]
        yield S[(S[i] + S[j]) & 0xFF]


def rc4_crypt(key: bytes, data: bytes) -> bytes:
    ks = rc4_ks(key)
    return bytes(b ^ next(ks) for b in data)


def extract_request_body_lines(ascii_stream: str) -> list[str]:
    """
    Try to extract the HTTP request body (client -> server) for /api/version.
    We look for the first GET/POST /api/version block and take the lines
    after the first blank line, until the next blank or 'HTTP/1.1'.
    """
    # Find the start of the request headers
    if "POST /api/version" in ascii_stream:
        idx = ascii_stream.index("POST /api/version")
    elif "GET /api/version" in ascii_stream:
        idx = ascii_stream.index("GET /api/version")
    else:
        return []

    chunk = ascii_stream[idx:]

    # Split headers and the rest
    if "\n\n" not in chunk:
        return []
    headers, rest = chunk.split("\n\n", 1)

    body_lines: list[str] = []
    for line in rest.splitlines():
        s = line.strip()
        if not s:
            # End of body or noise; if we already collected something, stop.
            if body_lines:
                break
            else:
                continue

        # Skip response start if we hit it
        if s.startswith("HTTP/1.1"):
            break

        # Skip tshark direction markers like "114", "205"
        if s.isdigit():
            continue

        body_lines.append(s)

    return body_lines


def main():
    pcap_path = sys.argv[1] if len(sys.argv) > 1 else PCAP_DEFAULT
    if not Path(pcap_path).exists():
        print(f"[!] PCAP not found: {pcap_path}")
        sys.exit(1)

    key = KEY_HEX.encode("ascii")
    print(f"[*] Using key: {KEY_HEX}")

    streams = get_api_streams(pcap_path)
    print(f"[*] Found {len(streams)} /api/version streams: {streams}")

    for sid in streams:
        print(f"\n=== tcp.stream {sid} ===")
        ascii_stream = get_stream_ascii(pcap_path, sid)
        body_lines = extract_request_body_lines(ascii_stream)

        if not body_lines:
            print("  [!] No candidate body lines found")
            continue

        print("  [*] Candidate body lines:")
        for line in body_lines:
            print("    ", line)

        # Try each line as base64 separately
        for idx, b64 in enumerate(body_lines):
            try:
                enc = base64.b64decode(b64, validate=True)
            except Exception:
                continue

            print(f"  [+] Line {idx} looks like valid base64 (len={len(enc)} bytes)")
            dec = rc4_crypt(key, enc)

            out_bin = Path(f"decoded_api_version_stream{sid}_line{idx}.bin")
            out_bin.write_bytes(dec)
            print(f"    -> Saved binary: {out_bin}")

            try:
                text = dec.decode("utf-8")
                out_txt = Path(f"decoded_api_version_stream{sid}_line{idx}.txt")
                out_txt.write_text(text, encoding="utf-8")
                print(f"    -> Saved UTF-8 text: {out_txt}")
            except UnicodeDecodeError:
                print("    -> Not UTF-8; only .bin saved")


if __name__ == "__main__":
    main()
