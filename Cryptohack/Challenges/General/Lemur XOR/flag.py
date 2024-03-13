from PIL import Image, ImageChops

im1 = Image.open("lemur_ed66878c338e662d3473f0d98eedbd0d.png")
im2 = Image.open("flag_7ae18c704272532658c10b5faad06d74.png")

im3 = ImageChops.add(ImageChops.subtract(im2, im1), ImageChops.subtract(im1, im2))
im3.show()
im3.save("./im3.png")
