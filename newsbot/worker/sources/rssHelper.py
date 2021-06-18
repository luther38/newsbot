from bs4 import BeautifulSoup
from newsbot.worker.common.requestContent import RequestContent


class IRssContent:
    """
    This interface is used to define how the RssReader can intagrate with sites witout a full source.
    """

    def __init__(self):
        pass

    def getArticleContent(self) -> str:
        """
        Checks the soup object and finds the content of the article.

        Returns: str
        """
        raise NotImplementedError


class RssCache:
    def cacheSite(self, soup: BeautifulSoup):
        self.soup = soup


class Engadget(IRssContent, RssCache):
    def __init__(self) -> None:
        pass

    def getArticleContent(self) -> str:
        content = self.soup.find(name="div", attrs={"id": "engadget-post-contents"})
        return content.text


class ArsTechnica(IRssContent, RssCache):
    def __init__(self) -> None:
        pass

    def getArticleContent(self) -> str:
        content = self.soup.find(
            name="div", attrs={"class": "article-content post-page"}
        )
        p = content.find_all(name="p")
        body = ""
        for i in p:
            body += i.text + "\r\n"
        return body


class HowToGeek(IRssContent):
    def __init__(self) -> None:
        self.rc = RequestContent()

    def getArticleContent(self) -> str:
        # c = self.soup.find
        pass
