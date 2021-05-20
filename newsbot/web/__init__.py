from os import environ
from flask import Flask, render_template
from flask.helpers import url_for
from newsbot.core.startup import CoreStartup
from newsbot.web.api import api, apiSources, apiDiscordWebHooks
from newsbot.web.ui import config, configDiscord, configSource
from newsbot.web.ui.config import config
from newsbot.web.ui.config.discord import configDiscord


def startCore() -> None:
    CoreStartup().start()

def start() -> Flask:
    #startCore()
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder="static",
        template_folder="templates",
    )
    app.register_blueprint(blueprint=api, url_prefix='/api')
    app.register_blueprint(blueprint=apiSources, url_prefix='/api/sources')
    app.register_blueprint(blueprint=apiDiscordWebHooks, url_prefix='/api/discordwebhooks')

    app.register_blueprint(blueprint=config, url_prefix="/config")
    app.register_blueprint(blueprint=configDiscord, url_prefix='/config/discord')
    app.register_blueprint(blueprint=configSource, url_prefix='/config/source')

    @app.route("/")
    def index() -> str:
        # return "Hello World"
        return render_template("index.html")

    return app