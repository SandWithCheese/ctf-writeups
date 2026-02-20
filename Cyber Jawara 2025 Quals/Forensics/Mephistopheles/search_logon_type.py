
import sys
import re

filename = 'dist/2025-12-24T152325_Compromised_DEVICE01/C/Windows/System32/winevt/logs/Security.evtx'

with open(filename, 'rb') as f:
    data = f.read()
    # Search for 'as3ng' in UTF-16LE
    user_pattern = 'as3ng'.encode('utf-16le')

    indices = [m.start() for m in re.finditer(re.escape(user_pattern), data)]
    for idx in indices:
        start = max(0, idx - 2000)
        end = min(len(data), idx + 2000)
        chunk = data[start:end]
        
        # Search for LogonType 10 or RemoteInteractive
        # Note: EventID 4624 usually has specific keywords
        
        decoded = chunk.decode('utf-16le', errors='ignore')
        if 'RemoteInteractive' in decoded and '4624' in decoded: # crude check
             print(f"--- Potential RDP Logon for as3ng at offset {idx} ---")
             # Try to find date similar to what we did before
             pass 
        
        # If we can just print the surrounding text, we can eyeball the timestamp
        if 'RemoteInteractive' in decoded:
             print(f"--- RDP Context at {idx} ---")
             lines = decoded.splitlines()
             # print a few lines around the match
             for i, line in enumerate(lines):
                 if 'as3ng' in line or 'RemoteInteractive' in line or '192.168.100.157' in line:
                     # print surrounding
                     print('\n'.join(lines[max(0, i-5):min(len(lines), i+5)]))
             print("--------------------------------------------------")
