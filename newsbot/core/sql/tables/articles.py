from sqlalchemy.orm.session import Session
from newsbot.core.sql import database
from newsbot.core.sql.exceptions import FailedToAddToDatabase
from newsbot.core.sql.tables import Articles

class ArticlesTable():
    def __init__(self, session: Session) -> None:
        self.setSession(session)
        pass
        
    def setSession(self, session: Session) -> None:
        self.s = session

    def __len__(self) -> int:
        i: int = 0
        try:
            for res in self.s.query(Articles):
                i = i + 1
        except Exception as e:
            pass
        return len(i)

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

    def clone(self, item: Articles) -> Articles:
        return Articles(
            siteName=item.siteName,
            sourceType=item.sourceType,
            sourceName=item.sourceName,
            tags=item.tags,
            title=item.tags,
            url = item.url,
            pubDate=item.pubDate,
            video=item.video,
            videoHeight=item.videoHeight,
            videoWidth=item.videoWidth,
            thumbnail=item.thumbnail,
            description=item.description,
            authorName=item.authorName,
            authorImage=item.authorImage
        )

    def add(self, item: Articles) -> None:
        try:
            self.s.add(item)
            self.s.commit()
        except FailedToAddToDatabase as e:
            print(f"Failed to add {item.name} to Source table! {e}")

    def exists(self, url: str) -> bool:
        """
        Check to see if the current record exists.
        """
        try:
            for res in self.s.query(Articles).filter(Articles.url == url):
                return True
        except Exception as e:
            pass
        return False