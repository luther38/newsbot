from typing import List
from newsbot import env
from newsbot.logger import Logger
from newsbot.sources.common import BSources, ISources, UnableToFindContent, UnableToParseContent
from newsbot.sql import Articles, Sources, DiscordWebHooks
from requests import get, Response
from bs4 import BeautifulSoup

class PogohubReader(ISources, BSources):
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        self.uri = "https://pokemongohub.net/rss"
        self.siteName: str = "Pokemon Go Hub"
        self.authorName: str = "Pokemon Go Hub"
        self.links: List[Sources] = list()
        self.hooks: List[DiscordWebHooks] = list()
        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False
        self.checkEnv(self.siteName)
        pass

#    def checkEnv(self) -> None:
#        # Check if site was requested.
#        self.outputDiscord = self.isDiscordEnabled(self.siteName)
#        if self.outputDiscord == True:
#            self.hooks = self.getDiscordList(self.siteName)
#
#        self.sourceEnabled = self.isSourceEnabled(self.siteName)
#        if self.sourceEnabled == True:
#            self.links = self.getSourceList(self.siteName)

    def getArticles(self) -> List[Articles]:
        for site in self.links:
            self.logger.debug(f"{site.name} - Checking for updates.")
            self.uri = site.url

            siteContent: Response = self.getContent()
            if siteContent.status_code != 200:
                raise UnableToFindContent(
                    f"Did not get status code 200.  Got status code {siteContent.status_code}"
                )

            bs: BeautifulSoup = self.getParser(requestsContent=siteContent)

            allArticles: List[Articles] = list()
            try:
                mainLoop = bs.contents[1].contents[1].contents

                for i in mainLoop:
                    if i.name == "item":
                        item: Articles = self.processItem(i)

                        # we are doing the check here to see if we need to fetch the thumbnail.
                        # if we have seen the link already, move on and save on time.
                        seenAlready = item.exists()
                        if seenAlready == False:
                            # get thumbnail
                            item.thumbnail = self.getArticleThumbnail(item.url)
                            allArticles.append(item)

                self.logger.debug(f"Pokemon Go Hub - Finished checking.")
            except Exception as e:
                self.logger.error(
                    f"Failed to parse articles from Pokemon Go Hub.  Chances are we have a malformed responce. {e}"
                )

        return allArticles

#    def getContent(self) -> Response:
#        try:
#            headers = self.getHeaders()
#            return get(self.uri, headers=headers)
#        except Exception as e:
#            self.logger.critical(f"Failed to collect data from {self.uri}. {e}")
#
#    def getParser(self, siteContent: Response) -> BeautifulSoup:
#        try:
#            return BeautifulSoup(siteContent.content, features="html.parser")
#        except Exception as e:
#            self.logger.critical(f"failed to parse data returned from requests. {e}")

    def processItem(self, item: object) -> Articles:
        a = Articles(
            siteName=self.siteName,
            authorName=self.authorName,
            tags="pokemon go hub, pokemon, go, hub, news",
        )

        for i in item.contents:
            if i.name == "title":
                a.title = i.next
            elif i.name == "link":
                a.url = self.removeHTMLTags(i.next)
            elif i.name == "pubdate":
                a.pubDate = i.next
            elif i.name == "category":
                a.tags = i.next
            elif i.name == "description":
                a.description = self.removeHTMLTags(i.next)
            elif i.name == "content:encoded":
                a.content = i.next
        return a

    def removeHTMLTags(self, text: str) -> str:
        tags = ("<p>", "</p>", "<img >", "<h2>")
        text = text.replace("\n", "")
        text = text.replace("\t", "")
        text = text.replace("<p>", "")
        text = text.replace("</p>", "\r\n")
        text = text.replace("&#8217;", "'")
        spans = re.finditer("(?<=<span )(.*)(?=>)", text)
        try:
            if len(spans) >= 1:
                print("money")
        except:
            pass

        return text

    def getArticleThumbnail(self, link: str) -> str:
        try:
            r = get(link)
            bs: BeautifulSoup = BeautifulSoup(r.content, features="html.parser")
            res = bs.find_all("img", class_="entry-thumb")
            return res[0].attrs["src"]
        except Exception as e:
            self.logger.error(f"Failed to pull Pokemon Go Hub thumbnail or {link}. {e}")
