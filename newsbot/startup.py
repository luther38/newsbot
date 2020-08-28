from newsbot import logger, env
from newsbot.outputs.discord import Discord
from newsbot.workers.worker import Worker
from newsbot.sources.ffxiv import FFXIVReader
from newsbot.sources.pso2 import PSO2Reader
from newsbot.sources.redditrss import RedditReader
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
        # tDiscord.start()

        s_ffxiv = FFXIVReader()
        w_ffxiv = Worker(s_ffxiv)
        t_ffxiv = Thread(target=w_ffxiv.init, name="Final Fantasy XIV")
        # t_ffxiv.start()

        s_pogo = PogohubReader()
        w_pogo = Worker(s_pogo)
        t_pogo = Thread(target=w_pogo.init, name="Pokemon Go Hub")
        t_pogo.start()

        s_pso2 = PSO2Reader()
        w_pso2 = Worker(s_pso2)
        t_pso2 = Thread(target=w_pso2.init, name="PSO2")
        # t_pso2.start()

        s_reddit = RedditReader()
        w_reddit = Worker(s_reddit)
        t_reddit = Thread(target=w_reddit.init, name="Reddit")
        # t_reddit.start()
