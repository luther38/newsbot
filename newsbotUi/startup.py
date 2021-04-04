from flask import Flask

class NewsbotUI():
    def __init__(self):
        self.app = Flask(
            __name__
            ,instance_relative_config=True
        )
        self.addBlueprints()
        self.startFlask()
        pass

    def getFlask(self) -> Flask:
        return self.app


    def addBlueprints(self) -> None:
        pass


    def startFlask(self) -> Flask:

        @self.app.route('/')
        def index() -> str:
            return "Hello World"