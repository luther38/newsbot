from newsbot import logger, env
from newsbot.outputs.discord import Discord
from newsbot.workers.worker import Worker
from newsbot.sources.ffxiv import FFXIVReader
from newsbot.sources.pso2 import PSO2Reader
from newsbot.sources.youtube import YoutubeReader
from newsbot.sources.reddit import RedditReader
from newsbot.sources.pokemongohub import PogohubReader
from newsbot.sources.instagram import InstagramReader
from newsbot.sources.twitter import TwitterReader

from newsbot.tables import Sources, DiscordWebHooks
from newsbot.initdb import InitDb
from threading import Thread


class Startup:
    def __init__(self) -> None:
        pass

    def startProgram(self) -> None:
        logger.info("NewsBot has started.")
        db = InitDb()
        db.runMigrations()
        db.clearOldRecords()
        db.runDatabaseTasks()

        # Turn on outputs first
        Thread(target=Discord().enableThread, name="Discord").start()

        Thread(target=Worker(FFXIVReader()).init, name="Final Fantasy XIV").start()
        Thread(target=Worker(PogohubReader()).init, name="Pokemon Go Hub").start()
        Thread(target=Worker(PSO2Reader()).init, name="PSO2").start()
        Thread(target=Worker(RedditReader()).init, name="Reddit").start()
        Thread(target=Worker(YoutubeReader()).init, name="Youtube").start()
        Thread(target=Worker(InstagramReader()).init, name="Instagram").start()
        Thread(target=Worker(TwitterReader()).init, name="Twitter").start()
