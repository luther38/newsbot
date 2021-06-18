from newsbot.core.logger import Logger
from newsbot.core.sql.tables import Sources, DiscordWebHooks, Articles
from newsbot.core.constant import SourceName
from newsbot.worker.sources.common import BSources, UnableToFindContent
from bs4 import BeautifulSoup
from typing import List
import re
from requests import get, Response


class PSO2Reader(BSources):
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        self.uri: str = "https://pso2.com/news"
        self.siteName: str = SourceName.PHANTASYSTARONLINE2.value
        self.authorName: str = f"{self.siteName} Official Site"
        self.links: List[Sources] = list()
        self.hooks: List[DiscordWebHooks] = list()
        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False
        self.checkEnv(self.siteName)
        pass

    def getArticles(self) -> List[Articles]:
        allArticles: List[Articles] = list()
        for site in self.links:
            self.logger.debug(f"{site.name} - Checking for updates.")

            siteContent: Response = self.getContent()
            if siteContent.status_code != 200:
                self.logger.error(
                    f"The returned content from {self.siteName} is either malformed or incorrect.  We got the wrong status code.  Expected 200 but got {siteContent.status_code}"
                )
            page: BeautifulSoup = self.getParser(requestsContent=siteContent)

            try:
                for news in page.find_all("li", {"class", "news-item all sr"}):
                    a = Articles(
                        siteName=self.siteName,
                        authorName=self.authorName,
                        sourceName="phantasystaronline2",
                        sourceType="phantasystaronline2",
                    )
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
                self.logger.error(f"PSO2 - Unable to find articles. {e}")

        self.logger.debug(f"{site.name} - Finished collecting articles")
        return allArticles

    def findNewsLinks(self, page: BeautifulSoup) -> BeautifulSoup:
        try:
            news = page.find_all(
                "ul", {"class", "news-section all-news announcement-section active"}
            )
            if len(news) != 1:
                self.logger.error(
                    f"Collected results from news-section but got more results then expected."
                )

            return news
        except Exception as e:
            self.logger.error(
                f"Failed to find news-section.  Did the site layout change? {e}"
            )

    def findListItems(self, news: BeautifulSoup) -> BeautifulSoup:
        try:
            for article in news.find_all("li", {"class", "news-item all sr"}):
                print(article)
            pass
        except UnableToFindContent as e:
            self.logger.error(f"{e}")
