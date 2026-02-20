
import re

filename = 'dist/2025-12-24T152325_Compromised_DEVICE01/C/Windows/System32/winevt/logs/Microsoft-Windows-Sysmon%4Operational.evtx'
ip = b'192.168.100.157'

with open(filename, 'rb') as f:
    data = f.read()

# Find all occurrences of the IP
indices = [m.start() for m in re.finditer(re.escape(ip), data)]

print(f"Found {len(indices)} occurrences of {ip}")

for idx in indices:
    start = max(0, idx - 100)
    end = min(len(data), idx + 200)
    chunk = data[start:end]
    
    # Try to decode as utf-16le (windows) or ascii
    try:
        print(f"--- Context at {idx} (UTF-16) ---")
        # Sysmon evtx uses UTF-16LE mostly for strings
        # We need to align to even bytes for utf-16
        s_aligned = start if start % 2 == 0 else start + 1
        print(data[s_aligned:end].decode('utf-16le', errors='ignore'))
    except:
        pass
        
    print(f"--- Context at {idx} (ASCII) ---")
    try:
        print(chunk.decode('ascii', errors='ignore'))
    except:
        pass
    print("--------------------------------------------------")
