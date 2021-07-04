from sqlalchemy.orm.session import Session
from newsbot.core.logger import Logger
from newsbot.core.sql.tables import Sources, DiscordWebHooks, Articles
from newsbot.core.constant import SourceName
from newsbot.worker.sources.common import BSources, UnableToFindContent
from newsbot.worker.sources.driver import BFirefox
from newsbot.worker.sources.exceptions import *
from bs4 import BeautifulSoup
from typing import List
from time import sleep
import re
from requests import get, Response


class PSO2Reader(BSources):
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        self.uri: str = "https://pso2.com/news"
        self.siteName: str = SourceName.PHANTASYSTARONLINE2.value
        self.authorName: str = f"Phantasy Star Online 2 Official Site"
        self.links: List[Sources] = list()
        self.hooks: List[DiscordWebHooks] = list()
        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False
        #self.checkEnv(self.siteName)
        self.session: Session = None
        pass

    def getArticles(self) -> List[Articles]:
        allArticles: List[Articles] = list()
        ngs = PSO2NGSReader()
        ngsPosts = ngs.getArticles()
        for post in ngsPosts:
            allArticles.append(post)

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
                        sourceName=self.siteName,
                        sourceType=self.siteName,
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

class PSO2NGSReader(BSources):
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        self.rootUrl = "https://ngs.pso2.com/news"
        pass

    def getArticles(self) -> List[Articles]:
        ngsPosts: List[Articles] = []
        ui = PSO2NGSUiHandler()
        html = ui.getPosts()
        soup = self.getParser(seleniumContent=html)
        items = soup.find_all('li', {"class", "news-item all sr active"})
        for item in items:
            a = Articles(
                siteName="Phantasy Star Online 2: New Genesis",
                sourceName=SourceName.PHANTASYSTARONLINE2.value,
                sourceType=SourceName.PHANTASYSTARONLINE2.value,
                url=self.getUrl(item=item),
                description=self.getDescription(item=item),
                authorName="Phantasy Star Online 2: New Genesis - Offical Site",
                pubDate= self.getDatePosted(item=item),
                title= self.getTitle(item=item),
                thumbnail= self.getThumbnail(item=item),
                tags='pso2ngs, news, ' + self.getTag(item=item)
            )
            ngsPosts.append(a)

            #pageContent = ui.getPageDetails(a.url)

        ui.driverClose()
        return ngsPosts

    def getThumbnail(self, item: BeautifulSoup) -> str:
        try:
            line: str = item.contents[1].attrs['style']
            if line != '':
                if 'background-image: url(' in line:
                    line = line.replace('background-image: url(', '')
                    line = line.replace(')', '')
                    return line
        except FailedToFindHtmlObject as e:
            self.logger.error(f"Attempted to find the Thumbnail for a PSO2NGS post, but was not found. {e}")

    def getTitle(self, item: BeautifulSoup) -> str:
        try:
            title = item.contents[3].contents[1].text
            return title
        except FailedToFindHtmlObject as e:
            self.logger.error(f"Attempted to find the Title for a PSO2NGS post, but was not found. {e}")

    def getDescription(self, item: BeautifulSoup) -> str:
        try:
            res = item.contents[3].contents[3].string
            return res
        except FailedToFindHtmlObject as e:
            self.logger.error(f"Attempted to find the post Description for a PSO2NGS post, but was not found. {e}")

    def getTag(self, item: BeautifulSoup) -> str:
        try:
            tag:str = item.contents[3].contents[5].contents[1].string
            return tag.lower()
        except FailedToFindHtmlObject as e:
            self.logger.error(f"Attempted to find the Title for a PSO2NGS post, but was not found. {e}")

    def getDatePosted(self, item: BeautifulSoup) -> str:
        try:
            datePosted: str = item.contents[3].contents[5].contents[5].string
            return datePosted
        except FailedToFindHtmlObject as e:
            self.logger.error(f"Attempted to find the DatePosted for a PSO2NGS post, but was not found. {e}")

    def getUrl(self, item:BeautifulSoup) -> str:
        try:
            res: str = item.contents[3].contents[5].contents[7].attrs['onclick']
            res = res.replace('(ShowDetails(', '')
            res = res.replace('))', '')
            res = res.replace("'", '')
            res = res.replace(' ', '')
            r = res.split(',')

            cat = f"{r[1]}s"
            page = r[0]

            url = f"{self.rootUrl}/{cat}/{page}"
            return url
        except FailedToFindHtmlObject as e:
            self.logger.error(f"Attempted to find the URL for a PSO2NGS post, but was not found. {e}")


class PSO2NGSUiHandler(BFirefox):
    """This class handles moving around the site."""
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        self.urlAgeGate = "https://ngs.pso2.com/agegate"
        self.urlNews = "https://ngs.pso2.com/news/latest"

    def getPosts(self) -> str:
        """Uses Selenium to navigate to the page where news can be found."""
        self.driver = self.driverStart()
        self.driverGoTo(self.urlAgeGate)
        passedAgeGate = self.passAgeGate()
        if passedAgeGate == False:
            return None

        self.driverGoTo(self.urlNews)
        #self.driverSaveScreenshot("ngs_news.png")
        html = self.driverGetContent()
        
        return html

    def passAgeGate(self) -> bool:
        curUrl = self.driverGetUrl()
        if "agegate" in curUrl:
            # handle the age gate
            self.clickAgeGateYear()
            self.submitAgeGateForm()
            sleep(10)
            newUrl = self.driverGetUrl()
            if newUrl != curUrl:
                self.logger.debug(f"Was moved to '{newUrl}'")
                return True
            else:
                self.logger.debug(f"Was not moved to a new page!")
                return False
        return True
    
    def clickAgeGateYear(self) -> None:
        self.logger.debug(f"Clicking on a year value.")
        yearEle = self.driverFindByXPath(xpath='/html/body/div/main/div/div/form/div/select[3]/option[41]')
        yearEle.click()
        #self.driverSaveScreenshot("ngs_agegate_year.png")

    def submitAgeGateForm(self) -> None:
        self.logger.debug(f"Submitting the form.")
        submitEle = self.driverFindByXPath(xpath="/html/body/div/main/div/div/form/input[1]")
        submitEle.click()
        sleep(10)
        #self.driverSaveScreenshot("ngs_agegate_submit.png")

    def getPageDetails(self, url: str) -> str:
        self.driverGoTo(uri=url)
        c: str = self.driverGetContent()
        return c
