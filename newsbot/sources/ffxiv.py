
from typing import List
import requests
from bs4 import BeautifulSoup
import re
from newsbot import logger, env
from newsbot.sources.rssreader import RSSReader
from newsbot.collections import RSSRoot, RSSArticle

class FFXIVReader(RSSReader):
    def __init__(self) -> None:
        self.uri: str = "https://na.finalfantasyxiv.com/lodestone/news/"
        self.baseUri: str = "https://na.finalfantasyxiv.com"
        self.siteName: str = "Final Fantasy XIV"
        self.links = list()
        self.hooks = list()

        self.checkEnv()
        pass
    
    def getArticles(self) -> RSSRoot:
        rss = RSSRoot()
        rss.link = self.uri
        rss.title = self.siteName

        for site in self.links:
            logger.debug(f"{self.siteName} - {site['tag']} - Checking for updates")
            self.uri = site['uri']
            page = self.getParser()

            a = RSSArticle()
            a.siteName = self.siteName
            if site['tag'] == "Topics":
                try:
                    for news in page.find_all("li", {"class", "news__list--topics ic__topics--list"}):
                        header = news.contents[0].contents
                        body = news.contents[1].contents
                        a.title = header[0].text
                        a.link = f"{self.baseUri}{header[0].contents[0].attrs['href']}"
                        #a.pubDate = header.contents[1].
                        a.thumbnail = body[0].contents[0].attrs['src']
                        a.description = body[0].contents[0].next_element.text
                        a.tags = 'Topics'

                        rss.articles.append(a)

                except Exception as e:
                    logger.error(e)
            
            if site['tag'] == 'Notices':
                try:
                    for news in page.find_all("li", {"class", "news__list"}):


            logger.debug("")
        return rss

    def checkEnv(self):
        self.hooks: List = env.ffxiv_hooks

        if env.ffxiv_news == True or env.ffxiv_all == True:
            self.links.append({
                'tag': 'Topics',
                'uri': 'https://na.finalfantasyxiv.com/lodestone/topics/'
            })
        
        if env.ffxiv_notices == True or env.ffxiv_all == True:
            self.links.append({
                'tag': 'Notices',
                'uri': 'https://na.finalfantasyxiv.com/lodestone/news/category/1'
            })
        
        if env.ffxiv_maintenance == True or env.ffxiv_all == True:
            self.links.append({
                'tag': "Maintenance",
                'uri': 'https://na.finalfantasyxiv.com/lodestone/news/category/2'
            })

        if env.ffxiv_updates == True or env.ffxiv_all == True:
            self.links.append({
                'tag': "Updates",
                'uri': "https://na.finalfantasyxiv.com/lodestone/news/category/3"
            })

        if env.ffxiv_status == True or env.ffxiv_status == True:
            self.links.append({
                'tag': 'Status',
                'uri': "https://na.finalfantasyxiv.com/lodestone/news/category/4"
            })
            
