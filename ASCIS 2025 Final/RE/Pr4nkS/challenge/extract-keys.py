#!/usr/bin/env python3
import subprocess
import re
import sys
from pathlib import Path

# Regex for 32 lowercase hex chars (your versions look like this)
HEX32_RE = re.compile(r"\b[a-f0-9]{32}\b")


def run(cmd):
    # Helper to run a shell command and get stdout as text
    return subprocess.check_output(cmd, text=True)


def get_stream_ids(pcap_path: str):
    """
    Use tshark to get all tcp.stream IDs for /get_latest_version requests
    to update.rnicrosoft.com.
    """
    cmd = [
        "tshark",
        "-r",
        pcap_path,
        "-Y",
        'ip.addr==192.168.89.133 && http.host=="update.rnicrosoft.com" && http.request.uri=="/get_latest_version"',
        "-T",
        "fields",
        "-e",
        "tcp.stream",
    ]
    out = run(cmd)
    streams = sorted(set(int(x) for x in out.split() if x.strip().isdigit()))
    return streams


def extract_key_from_stream(pcap_path: str, stream_id: int):
    """
    Follow TCP stream in ASCII and try to find a 32-hex key in the body.
    """
    cmd = [
        "tshark",
        "-r",
        pcap_path,
        "-qz",
        f"follow,tcp,ascii,{stream_id}",
    ]
    out = run(cmd)

    # We just regex-snipe any 32-char hex strings in the whole stream
    candidates = HEX32_RE.findall(out)
    # You’ll usually get exactly one, but return all just in case.
    return candidates


def main():
    if len(sys.argv) > 1:
        pcap_path = sys.argv[1]
    else:
        pcap_path = "svanm_2025.pcapng"

    if not Path(pcap_path).exists():
        print(f"[!] PCAP not found: {pcap_path}")
        sys.exit(1)

    print(f"[*] Using pcap: {pcap_path}")

    streams = get_stream_ids(pcap_path)
    print(f"[*] Found {len(streams)} candidate streams for /get_latest_version")

    all_keys = set()

    for sid in streams:
        print(f"[+] Analyzing tcp.stream == {sid} ...")
        keys = extract_key_from_stream(pcap_path, sid)
        for k in keys:
            all_keys.add(k)

    print("\n=== Unique candidate keys ===")
    print("CANDIDATE_KEYS = [")
    for k in sorted(all_keys):
        print(f'"{k}",')
    print("]")

    print(f"\n[*] Total unique keys: {len(all_keys)}")


if __name__ == "__main__":
    main()
