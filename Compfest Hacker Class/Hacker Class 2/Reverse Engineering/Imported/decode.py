import importlib

module = importlib.import_module("secret")
output = ""

while True:
    importlib.reload(module)
    char = module.c()
    output += char
    print(".", end="", flush=True)

    if char == "}":
        print()
        break

print(output)
