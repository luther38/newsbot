from flask import Blueprint, render_template, request
from .discord import configDiscord
from .sources import configSource

config = Blueprint(name="config", import_name=__name__, template_folder="templates")

@config.route("/")
def index() -> None:
    return render_template("config/index.html")



@config.route("/wizzard")
def wizzard() -> None:
    return render_template("config/wizzard.html")
