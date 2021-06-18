from typing import List
from newsbot.core.sql import database
from newsbot.core.sql.tables import Articles, DiscordQueue
from newsbot.core.sql.exceptions import FailedToAddToDatabase

class DiscordQueueTable():
    def __init__(self) -> None:
        self.s = database.newSession()
        
    #def __exit__(self) -> None:
    #    self.s.close()

    def __len__(self, siteName: str ) -> int:
        """
        Returns the number of rows based off the SiteName value provieded.
        """
        l = list()
        try:
            for res in self.s.query(Articles).filter(Articles.siteName == siteName):
                l.append(res)
        except Exception as e:
            pass
        return len(l)

    def convert(self, Article: Articles) -> DiscordQueue:
        q = DiscordQueue()

        q.siteName = Article.siteName
        q.title = Article.title
        q.link = Article.url
        q.tags = Article.tags
        q.thumbnail = Article.thumbnail
        q.description = Article.description
        q.video = Article.video
        q.videoHeight = Article.videoHeight
        q.videoWidth = Article.videoWidth
        q.authorName = Article.authorName
        q.authorImage = Article.authorImage
        q.sourceName = Article.sourceName
        q.sourceType = Article.sourceType

        return q

    def getQueue(self) -> List[DiscordQueue]:
        queue = list()
        try:
            for res in self.s.query(DiscordQueue):
                queue.append(res)
        except Exception as e:
            pass
        return queue

    def add(self, item: DiscordQueue) -> bool:
        res: bool = True
        try:
            self.s.add(item)
            self.s.commit()
        except FailedToAddToDatabase as e:
            print(f"Failed to add {item.title} to DiscorQueue table! {e}")
            res = False
        return res

    def remove(self, link: str) -> None:
        try:
            for d in self.s.query(DiscordQueue).filter(DiscordQueue.link == link):
                self.s.delete(d)
            self.s.commit()
        except Exception as e:
            print(f"{e}")

    def removeByLink(self, link: str) -> None:
        try:
            for d in self.s.query(DiscordQueue).filter(DiscordQueue.link == link):
                self.s.delete(d)
            self.s.commit()
        except Exception as e:
            print(f"{e}")
