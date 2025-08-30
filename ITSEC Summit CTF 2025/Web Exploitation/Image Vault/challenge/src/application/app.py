from flask import Flask
from application.routes.web import web_blueprint
from application.routes.api import api_blueprint

app = Flask(__name__, static_url_path="/static", static_folder="static")
app.config.from_object("application.config.Config")

app.register_blueprint(web_blueprint, url_prefix="/")
app.register_blueprint(api_blueprint, url_prefix="/api")
