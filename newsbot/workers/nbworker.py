 
from newsbot.collections import RSSArticle

class NBWorker:
    def __init__(self):
        pass

    def check(self) -> bool:
        raise NotImplementedError

    def init(self) -> None:
        """
        This is the entry point for the worker.  
        Once its turned on it will check the Source for new items.
        """
        raise NotImplementedError

    def sendToDiscord(self, article: RSSArticle):
        raise NotImplementedError