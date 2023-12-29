with open("cat.png", "rb") as f:
    isi = f.read()

with open("flag.png", "wb") as f:
    for i in range(0, len(isi), 4):
        payload = str(isi[i : i + 2])[4:6] + str(isi[i : i + 2])[8:10]

        payload += str(isi[i + 2 : i + 4])[4:6] + str(isi[i + 2 : i + 4])[8:10]

        print(int(payload, 2))
        payload = int(payload, 2)

        payload = int.to_bytes(payload)

        f.write(payload)
