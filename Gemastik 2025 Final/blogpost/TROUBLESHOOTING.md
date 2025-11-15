# Troubleshooting Guide

## ✅ FIXED: 500 Error on /login

### The Problem

You were getting this error:

```
172.18.0.1 - - [28/Oct/2025 04:40:05] "GET /login HTTP/1.1" 500 -
[2025-10-28 04:40:05,946] ERROR in app: Exception on /login [GET]
```

### Root Cause

**Flask expects a specific directory structure**, but the HTML and CSS files were in the wrong location:

```
❌ WRONG (what you had):
blogpost/
├── app.py
├── login.html        ← Flask can't find this
├── register.html     ← Flask can't find this
├── style.css         ← Flask can't find this
└── ...

✅ CORRECT (what Flask needs):
blogpost/
├── app.py
├── templates/        ← Flask looks here for HTML
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   └── ...
├── static/           ← Flask looks here for CSS/JS/images
│   └── style.css
└── ...
```

### The Fix

I've already fixed it! The files have been moved to the correct locations:

```bash
# Created directories
blogpost/templates/  ✓
blogpost/static/     ✓

# Moved files
templates/create_post.html  ✓
templates/index.html         ✓
templates/layout.html        ✓
templates/login.html         ✓
templates/profile.html       ✓
templates/register.html      ✓
templates/view_post.html     ✓
static/style.css             ✓
```

### Next Steps

Now you need to **rebuild and restart** your Docker container:

```bash
cd "/home/sandwicheese/ctf-writeups/Gemastik 2025 Final/blogpost"

# Stop the current container
docker-compose down

# Rebuild with the new directory structure
docker-compose build

# Start the container
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Verify It Works

```bash
# Test the login page
curl http://localhost:4413/login

# Should return HTML, not a 500 error
```

### Why This Happened

Flask has conventions:

- **`templates/`** directory for Jinja2 HTML templates
- **`static/`** directory for CSS, JavaScript, images, etc.

When you call `render_template("login.html")`, Flask looks in `templates/login.html`.

### Alternative: If You Had the RAR Archive

If you had extracted from `blogpost.rar`, the structure was probably already correct. But somehow the files ended up in the root directory.

## Common Docker Issues

### Issue: Port Already in Use

```
Error: bind: address already in use
```

**Solution:**

```bash
# Find what's using the port
sudo lsof -i :4413

# Kill the process or change the port in docker-compose.yml
```

### Issue: Permission Denied

```
Error: Cannot connect to the Docker daemon
```

**Solution:**

```bash
# Add your user to docker group
sudo usermod -aG docker $USER

# Log out and back in, or:
newgrp docker
```

### Issue: Database Not Initialized

```
Error: no such table: users
```

**Solution:**
The `entrypoint.sh` should handle this, but if not:

```bash
# Enter the container
docker exec -it ctf_web bash

# Initialize database
sqlite3 /data/app.db < /app/init_db.sql
```

### Issue: Flag File Missing

```
flag not found
```

**Solution:**
The `entrypoint.sh` creates the flag. Check if it ran:

```bash
docker exec -it ctf_web cat /app/flag.txt
# Should show: GEMASTIK{...}
```

## Testing After Fix

### 1. Check if container is running

```bash
docker ps | grep ctf_web
```

### 2. Test all endpoints

```bash
BASE_URL="http://localhost:4413"

# Should return HTML (200 OK)
curl -I $BASE_URL/login
curl -I $BASE_URL/register
curl -I $BASE_URL/

# Should redirect to login (302)
curl -I $BASE_URL/profile
```

### 3. Check container logs

```bash
docker-compose logs --tail=50
```

### 4. Enter container to debug

```bash
docker exec -it ctf_web bash

# Inside container:
ls -la /app/templates/
ls -la /app/static/
cat /app/flag.txt
sqlite3 /data/app.db "SELECT * FROM users;"
```

## Still Having Issues?

### Check Dockerfile

Make sure the Dockerfile copies everything:

```dockerfile
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app     # This should copy templates/ and static/
```

### Check app.py Template Path

The app.py should have this (it does):

```python
app = Flask(__name__)  # Flask will look for templates/ by default
```

### Manual Verification

```bash
# Build container
docker build -t blogpost-test .

# Run and check structure
docker run -it blogpost-test bash
ls -la /app/templates/
ls -la /app/static/
```

## Summary

**The issue was simple**: Flask couldn't find the template files because they weren't in the `templates/` directory.

**The fix was simple**: Move HTML files to `templates/` and CSS to `static/`.

**What to do now**: Rebuild your Docker container with `docker-compose build && docker-compose up`.

You should now be able to access:

- http://localhost:4413/login ✓
- http://localhost:4413/register ✓
- http://localhost:4413/ (redirects to login) ✓

And run the exploit scripts:

```bash
python3 dapur.py localhost 4413
```

Happy hacking! 🎯

