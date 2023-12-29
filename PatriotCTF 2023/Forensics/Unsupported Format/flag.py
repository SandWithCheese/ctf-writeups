with open("Flag.jpg", "rb") as f:
    content = f.read()

with open("New_Flag.jpg", "wb") as f:
    f.write(content[:2569] + content[2731:])
