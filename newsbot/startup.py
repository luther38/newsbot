from newsbot import env
from newsbot.logger import Logger
from newsbot.sources import (
    FFXIVReader,
    PSO2Reader,
    PogohubReader,
    YoutubeReader,
    RedditReader,
    InstagramReader,
    TwitchReader,
    TwitterReader,
    RssReader,
)
from newsbot.outputs.discord import Discord
from newsbot.workers.worker import Worker
from newsbot.initdb import InitDb
from threading import Thread


class Startup:
    def __init__(self) -> None:
        self.startProgram()
        pass

    def startProgram(self) -> None:
        logger = Logger(__class__)
        db = InitDb()
        logger.info("Newsbot is starting up...")
        db.runMigrations()
        db.runDatabaseTasks()
        logger.info("Newsbot start up has finished.")
        
        ## Turn on outputs first
        logger.info("Turning on output monitors.")
        Thread(target=Discord().enableThread, name="Discord").start()

        logger.info("Turning on source monitors.")
        Thread(target=Worker(FFXIVReader()).init, name="Final Fantasy XIV").start()
        # Thread(target=Worker(PogohubReader()).init, name="Pokemon Go Hub").start()
        # Thread(target=Worker(PSO2Reader()).init, name="PSO2").start()
        # Thread(target=Worker(RedditReader()).init, name="Reddit").start()
        # Thread(target=Worker(YoutubeReader()).init, name="Youtube").start()
        # Thread(target=Worker(InstagramReader()).init, name="Instagram").start()
        # Thread(target=Worker(TwitterReader()).init, name="Twitter").start()
        # Thread(target=Worker(TwitchReader()).init, name="Twitch").start()
        # Thread(target=Worker(RssReader()).init, name="RSS").start()
