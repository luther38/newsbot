from typing import List
from newsbot.collections import RSSArticle


class Outputs:
    def __init__(self, articles: List[RSSArticle]):
        self.articles = articles
        pass

    def sendMessage(self) -> None:
        raise NotImplementedError
