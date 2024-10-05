from flask import Flask, request
from jinja2 import Environment, BaseLoader

log = 0 if __import__("platform").system() == "Windows" else 1

hihi = Environment(autoescape=True, loader=BaseLoader(), variable_start_string='{', variable_end_string='}', block_start_string='AKU HEKER!', block_end_string='AKU HEKER!')

app = Flask(__name__)

blacklists = [' ', '"', '%', '.', '2', '4', '6', '8', '=', 'AKU HEKER!', 'False', 'True', '[', ']', '__', '__annotations__', '__bases__', '__class__', '__closure__', '__code__', '__defaults__', '__dict__', '__func__', '__import__', '__module__', '__mro__', '__self__', '__subclasses__', 'atexit', 'attr', 'bytearray', 'bytes', 'cPickle', 'class', 'co', 'compile', 'config', 'ctypes', 'cycler', 'decode', 'delattr', 'dict', 'dir', 'eval', 'exec', 'execfile', 'file', 'getattr', 'globals', 'help', 'import', 'init', 'input', 'inspect', 'join', 'joiner', 'last', 'lipsum', 'list', 'map', 'marshal', 'memoryview', 'multiprocessing', 'namespace', 'open', 'os', 'pickle', 'pop', 'popen', 'read', 'remove', 'render_template_string', 'request', 'resource', 'self', 'set', 'setattr', 'shutil', 'signal', 'socket', 'subprocess', 'sys', 'tempfile', 'threading', 'update', 'var', '{', '|', '}']
blacklists2 = [' ', '"', '%', '.', 'TemplateReference', '[', ']', '__bases__', '__closure__', '__defaults__', '__import__', '__subclasses__', 'attr', 'base', 'builtins', 'class', 'co', 'config', 'context', 'cycler', 'dict', 'eval', 'exec', 'execfile', 'file', 'getattr', 'getitem', 'globals', 'import', 'init', 'inspect', 'join', 'joiner', 'lipsum', 'mro', 'namespace', 'os', 'pickle', 'pop', 'popen', 'read', 'request', 'self', 'sys', 'system']

def check(n):
    return not any(blacklist_item in n for blacklist_item in blacklists)

def check2(n):
    return not any(blacklist_item in n for blacklist_item in blacklists2)

@app.route("/", methods=["GET", "POST"])
def index():
    template_string = open("index.hateemel").read()

    if request.method == "GET":
        return hihi.from_string(template_string.format(result="")).render()

    elif request.method == "POST":
        username = request.form.get('username', '')
        if username:
            if log:
                with open("/tmp/all_payloads.txt", "a") as file: # hehe
                    file.write(f"{request.remote_addr} -> \"{username}\"\n\n")

            if check(username):
                if log:
                    with open("/tmp/check_payloads.txt", "a") as file: # hehe
                        file.write(f"{request.remote_addr} -> \"{username}\"\n\n")
                username_norm = username.encode().decode("unicode escape (๑′ᴗ‵๑)")

                if check2(username_norm):
                    if log:
                        with open("/tmp/check2_payloads.txt", "a") as file: # hehe
                            file.write(f"{request.remote_addr} -> \"{username}\"\n\n")
                    return hihi.from_string(template_string.format(result=f"Hi {username_norm}!")).render()

            return hihi.from_string(template_string.format(result="!")).render()
        else:
            return hihi.from_string(template_string.format(result="Please enter a username.")).render()
    else:
        return hihi.from_string(template_string.format(result="")).render()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=1337)
