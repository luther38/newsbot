
from newsbot import logger, env
from newsbot.outputs.discord import Discord
from newsbot.workers.worker import Worker
from newsbot.sources.ffxiv import FFXIVReader
from newsbot.sources.pso2 import PSO2Reader
from newsbot.sources.redditrss import RedditReader
from newsbot.sources.pokemongohub import PogohubReader
from newsbot.tables import Sources, DiscordWebHooks
from threading import Thread

class Startup:
    def __init__(self) -> None:
        pass

    def startProgram(self) -> None:
        logger.info("NewsBot has started.")
        self.runDatabaseTasks()

        # Turn on outputs first
        oDiscord = Discord()
        tDiscord = Thread(target=oDiscord.enableThread, name="Discord")
        tDiscord.start()

        s_ffxiv = FFXIVReader()
        w_ffxiv = Worker(s_ffxiv)
        t_ffxiv = Thread(target=w_ffxiv.init, name="Final Fantasy XIV")
        #t_ffxiv.start()

        s_pogo = PogohubReader()
        w_pogo = Worker(s_pogo)
        t_pogo = Thread(target=w_pogo.init, name="Pokemon Go Hub")
        #t_pogo.start()

        s_pso2 = PSO2Reader()
        w_pso2 = Worker(s_pso2)
        t_pso2 = Thread(target=w_pso2.init, name="PSO2")
        #t_pso2.start()

        s_reddit = RedditReader()
        w_reddit = Worker(s_reddit)
        t_reddit = Thread(target=w_reddit.init, name="Reddit")
        t_reddit.start()

    def runDatabaseTasks(self):
        #clear our the table cache from last startup
        Sources().clearTable()
        DiscordWebHooks().clearTable()

        #Inject new values based off env values
        Sources(name="Pokemon Go Hub", url="https://pokemongohub.net/").add()
        for i in env.pogo_hooks:
            DiscordWebHooks(name="Pokemon Go Hub", key=i).add()

        Sources(name="Phantasy Star Online 2", url="https://pso2.com/news").add()
        for i in env.pso2_hooks:
            DiscordWebHooks(name="Phantasy Star Online 2", key=i).add()

        Sources(name="Final Fantasy XIV", url="https://na.finalfantasyxiv.com").add()
        for i in env.ffxiv_hooks:
            DiscordWebHooks(name="Final Fantasy XIV", key=i).add()

        r1 = f"Reddit {env.redditSub01}"
        Sources(name=r1, url=f"https://reddit.com/r/{env.redditSub01}").add()
        for i in env.redditHook01:
            DiscordWebHooks(name=r1, key=i).add()