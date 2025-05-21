import UnityPy
from PIL import Image
import os

env = UnityPy.load("./Flappy Bird_Data/sharedassets0.assets")

sprites = []
max_width = 0
max_height = 0

# Collect sprite images and their original positions
for obj in env.objects:
    if obj.type.name == "Sprite":
        sprite = obj.read()
        name = sprite.m_Name
        if name.startswith("huruf_"):
            img = sprite.image
            x, y = int(sprite.m_Rect.x), int(sprite.m_Rect.y)
            width, height = img.size
            sprites.append((img, x, y))
            max_width = max(max_width, x + width)
            max_height = max(max_height, y + height)

# Create a blank canvas based on max extents
canvas = Image.new("RGBA", (max_width, max_height), (0, 0, 0, 0))

# Paste each sprite at its original (x, y)
for img, x, y in sprites:
    canvas.paste(img, (x, y), img)

# Save the result
output_path = "reconstructed_sprite_sheet.png"
canvas.save(output_path)
print(f"Sprite sheet reconstructed and saved to: {output_path}")
