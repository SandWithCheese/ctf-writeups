from flask import Flask, render_template_string, request

app = Flask(__name__)

restricted = ["config","class","application","globals","getitem","import","popen","read","system","subclasses","init","items","query","self","base","_","/","shell","flag","cat","strings","builtins","eval","subprocess","stdout","for","IFS","getClass","communicate","options","id","dump","mro","filter","newInstance","iteritems","endfor"]

@app.route("/", methods=['POST', 'GET'])
def home():
    name = ''
    greeting = ''
    if request.method == 'POST':
        name = request.form.get('name', '')
        for i in restricted:
            if i in name:
                return "Ga Dlu!"
        if name == "Heisenberg" or name == "Walter White":
            greeting = "You're Goddamn Right!"
        else:
            greeting = "Hello, " + name + "!"

    template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">
        <meta charset="UTF-8" />
        <title>Say my name</title>
        <style>
            body {
                background-image: url("https://i.pinimg.com/736x/2c/f8/c2/2cf8c25a09e92a4c380c409c1652228b.jpg");
                background-size: cover;
                background-repeat: no-repeat;
                margin: 0;
            }
        </style>
    </head>
    <body>
        <div class="d-flex align-items-center justify-content-center" style="height: 100vh;">
            <form method="POST" class="container">
                <div class="form-group row">
                    <div class="col-sm-12 col-md-8 col-lg-6 mx-auto">
                        <h1 class="display-4 text-white text-center pb-2">Say my name</h1>
                        <input type="text" class="form-control" name="name" placeholder="Enter your name" maxlength="11" required>
                    </div>
                </div>
                <div class="form-group row">
                    <div class="col-sm-12 col-md-8 col-lg-6 mx-auto">
                        <input type="submit" class="btn btn-primary btn-block" value="Submit">
                    </div>
                </div>
                <div class="form-group row">
                    <div class="container text-center">
                        <h1 class="display-5 text-white">''' + greeting + '''</h1>
                    </div>
                </div>
            </form>
        </div>
    </body>
    </html>'''
    return render_template_string(template)


if __name__ == '__main__':
    app.run(port=8181)
