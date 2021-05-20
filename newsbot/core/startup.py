from newsbot.core.logger import Logger
from newsbot.core.initdb import InitDb

class CoreStartup:
    def start(self) -> None:
        logger = Logger(__class__)
        db = InitDb()
        db.runMigrations()
        logger.info("Newsbot is starting up...")
        db.runDatabaseTasks()
        logger.info("Newsbot start up has finished.")
