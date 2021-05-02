from flask import Flask, render_template
from flask.helpers import url_for
from newsbotUi.config import config
from newsbotUi.config.discord import configDiscord

app = Flask(
    __name__,
    instance_relative_config=True,
    static_folder="static",
    template_folder="templates",
)

app.register_blueprint(blueprint=config, url_prefix="/config")
app.register_blueprint(blueprint=configDiscord, url_prefix='/config/discord')

@app.route("/")
def index() -> str:
    # return "Hello World"
    return render_template("index.html")
