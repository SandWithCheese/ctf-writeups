
import re

filename = 'sysmon.txt'

# Regex for IP address
ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

# We want to find blocks associated with AnsiArtInstaller.exe or ansi_art.exe
# and then find IPs and Ports.

# Since the file structure is loose (strings output), we scan line by line
# and keep a context window.

interesting_exes = ['AnsiArtInstaller.exe', 'ansi_art.exe', 'program.banner', 'rundll32.exe', 'System.dll']
context_window = []
window_size = 40

found_connections = []

with open(filename, 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    line = line.strip()
    
    # Maintain context
    context_window.append(line)
    if len(context_window) > window_size:
        context_window.pop(0)
    
    # Check if we found an interesting executable in the recent window
    has_interesting_exe = any(exe in x for x in context_window for exe in interesting_exes)
    
    if has_interesting_exe:
        # Look for potential IPs in the current line
        ips = ip_pattern.findall(line)
        for ip in ips:
            # Ignore local broadcast/multicast/localhost
            if ip.startswith('224.') or ip == '127.0.0.1' or ip.startswith('169.254') or ip == '0.0.0.0' or ip == '255.255.255.255':
                continue
            
            # Check if we can find a port nearby
            # Ports are usually 1-5 digit numbers, often on their own line or near the IP.
            # In Sysmon Event 3, SourcePort is usually before DestIp, DestPort is after DestIp.
            
            # Let's print the context to examine manually
            print(f"--- Possible Connection context at line {i} ---")
            for c in context_window:
                print(c)
            # Print a few future lines too
            future = lines[i+1:i+10]
            for f_line in future:
                print(f_line.strip())
            print("-----------------------------------------------")
            
            # Clear window so we don't print same block repeatedly
            context_window = []

