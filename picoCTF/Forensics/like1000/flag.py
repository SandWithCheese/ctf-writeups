import tarfile

i = 999

while i > 0:
    f = tarfile.open(f"{i}.tar")
    f.extractall(".")
    i -= 1
