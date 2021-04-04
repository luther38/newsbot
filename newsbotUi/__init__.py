from flask import Flask, render_template
from newsbotUi.config import config

def start_flask() -> Flask:
    app = Flask(
        __name__
        ,instance_relative_config=True
        ,static_folder="static"
        ,template_folder="templates"
    )

    app.register_blueprint(blueprint=config, url_prefix='/config')

    @app.route('/')
    def index() -> str:
        #return "Hello World"
        return render_template("index.html")
    
    return app
