import zipfile

for i in range(100000, 999999):
    with zipfile.ZipFile('flag.zip') as zf:
        try:
            zf.extractall(pwd=str(i).encode())
            print(f"Found password: {i}")
            break
        except:
            print(i)
            pass