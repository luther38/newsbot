import newsbot
from newsbot.sources.pokemongohub import RSSPogohub
from newsbot.outputs.discord import Discord
from newsbot.collections import RSSRoot
from time import sleep


class PoGoHubWorker:
    def __init__(self) -> None:
        self.settings = newsbot.env
        pass

    def checkup(self) -> bool:
        # This checks to ensure that we want to use this source.
        if len(self.settings.pogo_hooks) >= 1:
            return True

    def init(self) -> None:
        runThread: bool = self.checkup()
        if runThread == True:
            while True:
                # TODO Logger
                print(f"Pokemon Go Hub - Thread Started")
                pogo = RSSPogohub()
                pogoNews: RSSRoot = pogo.getArticles()

                # TODO Logger
                print(f"Pokemon Go Hub - Collected {len(pogoNews.articles)}(s) to send")

                # Send to outputs

                # Check if we have any webhooks to send to.
                if len(self.settings.pogo_hooks) >= 1:
                    for i in pogoNews.articles:
                        d = Discord(i, self.settings.pogo_hooks, "Pokemon Go Hub")
                        d.sendMessage()
                        sleep(self.settings.discord_delay_seconds)

                sleep(self.settings.interval_seconds)

        else:
            print(
                "Did not have enough to enable Pokemon Go Hub Source.  Thread will exit."
            )
