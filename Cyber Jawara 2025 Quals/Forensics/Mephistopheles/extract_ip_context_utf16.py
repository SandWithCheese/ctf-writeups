
import re

filename = 'dist/2025-12-24T152325_Compromised_DEVICE01/C/Windows/System32/winevt/logs/Microsoft-Windows-Sysmon%4Operational.evtx'
ip_str = '192.168.100.157'
ip_utf16 = ip_str.encode('utf-16le')

with open(filename, 'rb') as f:
    data = f.read()

# Find all occurrences of the IP
indices = [m.start() for m in re.finditer(re.escape(ip_utf16), data)]

print(f"Found {len(indices)} occurrences of {ip_str} (UTF-16LE)")

for idx in indices:
    start = max(0, idx - 200)
    end = min(len(data), idx + 200)
    
    # Try to decode as utf-16le (windows)
    s_aligned = start if start % 2 == 0 else start + 1
    
    print(f"--- Context at {idx} ---")
    try:
        raw_chunk = data[s_aligned:end]
        decoded = raw_chunk.decode('utf-16le', errors='replace')
        # Replace newlines with spaces for compact view
        print(decoded.replace('\r', ' ').replace('\n', ' '))
    except Exception as e:
        print(f"Error decoding: {e}")
    print("--------------------------------------------------")
