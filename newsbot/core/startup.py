from newsbot.core.logger import Logger
from newsbot.core.initdb import InitDb

class Startup:
    def __init__(self) -> None:
        self.startProgram()
        pass

    def startProgram(self) -> None:
        logger = Logger(__class__)
        db = InitDb()
        db.runMigrations()
        logger.info("Newsbot is starting up...")
        db.runDatabaseTasks()
        logger.info("Newsbot start up has finished.")
