from newsbot import logger, env
from newsbot.sources.isources import ISources, UnableToFindContent
from newsbot.tables import Sources, DiscordWebHooks, Articles
from newsbot.collections import RSSArticle, RSSRoot, RssArticleImages, RssArticleLinks
from bs4 import BeautifulSoup
from typing import List
import re
from requests import get, Response


class PSO2Reader(ISources):
    def __init__(self) -> None:
        self.uri: str = "https://pso2.com/news"
        self.siteName: str = "Phantasy Star Online 2"
        self.links = list()
        self.hooks = list()
        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False
        self.checkEnv()
        pass

    def getArticles(self) -> List[Articles]:
        allArticles: List[Articles] = list()
        for site in self.links:
            logger.debug(f"{site.name} - Checking for updates.")
            self.uri = site.url

            siteContent: Response = self.getContent()
            if siteContent.status_code != 200:
                logger.error(
                    f"The returned content from {self.siteName} is either malformed or incorrect.  We got the wrong status code.  Expected 200 but got {siteContent.status_code}"
                )
            page: BeautifulSoup = self.getParser(siteContent)

            try:
                for news in page.find_all("li", {"class", "news-item all sr"}):
                    a = Articles()
                    a.siteName = "Phantasy Star Online 2"
                    a.thumbnail = re.findall(
                        "url[(](.*?)[)]", news.contents[1].attrs["style"]
                    )[0]

                    nc = news.contents[3].contents
                    a.title = nc[1].text
                    a.description = nc[3].text

                    bottom = nc[5].contents
                    a.tags = bottom[1].text
                    a.pubDate = bottom[5].text

                    link = re.findall(
                        r"ShowDetails\('(.*?)'", bottom[7].attrs["onclick"],
                    )[0]
                    # tells us the news type and news link
                    cat = bottom[1].text.lower()
                    if " " in cat:
                        cat = cat.replace(" ", "-")

                    a.url = f"{self.uri}/{cat}/{link}"

                    allArticles.append(a)
            except UnableToFindContent as e:
                logger.error(f"PSO2 - Unable to find articles. {e}")

        logger.debug(f"{site.name} - Finished collecting articles")
        return allArticles

    def findNewsLinks(self, page: BeautifulSoup) -> BeautifulSoup:
        try:
            news = page.find_all(
                "ul", {"class", "news-section all-news announcement-section active"}
            )
            if len(news) != 1:
                logger.error(
                    f"Collected results from news-section but got more results then expected."
                )

            return news
        except Exception as e:
            logger.error(
                f"Failed to find news-section.  Did the site layout change? {e}"
            )

    def findListItems(self, news: BeautifulSoup) -> BeautifulSoup:
        try:
            for article in news.find_all("li", {"class", "news-item all sr"}):
                print(article)
            pass
        except UnableToFindContent as e:
            logger.error(f"{e}")

    def checkEnv(self) -> None:
        self.isSourceEnabled()
        self.isDiscordOutputEnabled()

    def isSourceEnabled(self) -> None:
        res = Sources(name=self.siteName).findAllByName()
        if len(res) >= 1:
            self.links.append(res[0])
            self.sourceEnabled = True

    def isDiscordOutputEnabled(self) -> None:
        dwh = DiscordWebHooks(name=self.siteName).findAllByName()
        if len(dwh) >= 1:
            self.outputDiscord = True
            for i in dwh:
                self.hooks.append(i)

    def getContent(self) -> Response:
        try:
            headers = self.getHeaders()
            r = get(self.uri, headers=headers)
            return r
        except Exception as e:
            logger.critical(f"Failed to collect data from {self.uri}. {e}")

    def getParser(self, siteContent: Response) -> BeautifulSoup:
        try:
            return BeautifulSoup(siteContent.content, features="html.parser")
        except Exception as e:
            logger.critical(f"failed to parse data returned from requests. {e}")
