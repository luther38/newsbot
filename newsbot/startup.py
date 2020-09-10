from newsbot import logger, env
from newsbot.outputs.discord import Discord
from newsbot.workers.worker import Worker
from newsbot.sources.ffxiv import FFXIVReader
from newsbot.sources.pso2 import PSO2Reader
from newsbot.sources.youtube import YoutubeReader
from newsbot.sources.reddit import RedditReader
from newsbot.sources.pokemongohub import PogohubReader
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
        oDiscord = Discord()
        tDiscord = Thread(target=oDiscord.enableThread, name="Discord")
        tDiscord.start()

        w_ffxiv = Worker(FFXIVReader())
        t_ffxiv = Thread(target=w_ffxiv.init, name="Final Fantasy XIV")
        t_ffxiv.start()

        w_pogo = Worker(PogohubReader())
        t_pogo = Thread(target=w_pogo.init, name="Pokemon Go Hub")
        t_pogo.start()

        w_pso2 = Worker(PSO2Reader())
        t_pso2 = Thread(target=w_pso2.init, name="PSO2")
        t_pso2.start()

        w_reddit = Worker(RedditReader())
        t_reddit = Thread(target=w_reddit.init, name="Reddit")
        t_reddit.start()

        w_youtube = Worker(YoutubeReader())
        t_youtube = Thread(target=w_youtube.init, name="Youtube")
        t_youtube.start()
