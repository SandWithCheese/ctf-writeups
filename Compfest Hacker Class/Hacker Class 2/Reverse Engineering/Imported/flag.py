import importlib

module = importlib.import_module("new_secret")
output = ""

while True:
    print(f"{output=}")
    with open("new_secret.py", "r") as f:
        lines = f.readlines()
        lines.pop(-6)
        lines.pop(-6)
        # lines.pop(-7)
        # print(lines)
    # break
    with open("new_secret.py", "w") as f:
        f.writelines(lines)

    importlib.reload(module)
    char = module.c()
    output += char
    print(".", end="", flush=True)

    if char == "}":
        print()
        break

print(output)
