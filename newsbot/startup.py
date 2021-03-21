from newsbot import env
from newsbot.logger import Logger
from newsbot.sources import (
    FFXIVReader
    ,PSO2Reader
    ,PogohubReader
    ,YoutubeReader
    ,RedditReader
    ,InstagramReader
    ,TwitchReader
    ,TwitterReader
    ,RssReader
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
        db = InitDb()
        db.runMigrations()
        Logger(__class__).info("NewsBot has started.")
        db.clearOldRecords()
        db.runDatabaseTasks()

        # Turn on outputs first
        Thread(target=Discord().enableThread, name="Discord").start()

        Thread(target=Worker(FFXIVReader()).init, name="Final Fantasy XIV").start()
        Thread(target=Worker(PogohubReader()).init, name="Pokemon Go Hub").start()
        Thread(target=Worker(PSO2Reader()).init, name="PSO2").start()
        Thread(target=Worker(RedditReader()).init, name="Reddit").start()
        Thread(target=Worker(YoutubeReader()).init, name="Youtube").start()
#        Thread(target=Worker(InstagramReader()).init, name="Instagram").start()
        Thread(target=Worker(TwitterReader()).init, name="Twitter").start()
        Thread(target=Worker(TwitchReader()).init, name="Twitch").start()
        Thread(target=Worker(RssReader()).init, name="RSS").start()