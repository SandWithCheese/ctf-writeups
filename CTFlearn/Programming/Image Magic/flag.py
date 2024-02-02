from PIL import Image

img = Image.open("out copy.jpg")

width, height = img.size
new_height = width // 304
new_image = Image.new("RGB", (304, new_height))

col = 1
for x in range(0, width, new_height):
    block = img.crop((x, 0, x + new_height, height))

    # rotate block
    block = block.rotate(-90, expand=True)

    # save block
    new_image.paste(block, (col, 0))
    col += 1


new_image.save("flag.jpg")
