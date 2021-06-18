from threading import Thread
from newsbot.core.logger import Logger
from newsbot.worker.workers import Worker
from newsbot.worker.outputs import Discord
from newsbot.worker.sources import (
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

class NewsbotWorker():
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        pass

    def start(self) -> bool:
        ## Turn on outputs first
        self.logger.info("Turning on output monitors.")
        Thread(target=Discord().enableThread, name="Discord").start()

        self.logger.info("Turning on source monitors.")
        Thread(target=Worker(FFXIVReader()).init, name="Final Fantasy XIV").start()
        Thread(target=Worker(PogohubReader()).init, name="Pokemon Go Hub").start()
        Thread(target=Worker(PSO2Reader()).init, name="PSO2").start()
        Thread(target=Worker(RedditReader()).init, name="Reddit").start()
        Thread(target=Worker(YoutubeReader()).init, name="Youtube").start()
        Thread(target=Worker(InstagramReader()).init, name="Instagram").start()
        Thread(target=Worker(TwitterReader()).init, name="Twitter").start()
        Thread(target=Worker(TwitchReader()).init, name="Twitch").start()
        Thread(target=Worker(RssReader()).init, name="RSS").start()

        return True