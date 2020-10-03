from typing import List
from newsbot import logger, env
from newsbot.sources.isources import ISources, UnableToFindContent, UnableToParseContent
from newsbot.tables import Articles, Sources, DiscordWebHooks
from requests import get, Response
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
from tweepy import AppAuthHandler, API, Cursor
from os import getenv
from time import sleep

class TwitterReader(ISources):
    def __init__(self):
        self.uri: str = "https://twitter.com"
        self.baseUri = self.uri
        self.siteName: str = "Twitter"

        self.links: List[Sources] = list()
        self.hooks: List[DiscordWebHooks] = list()

        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False
        #self.driver: Chrome = Chrome()
        self.checkEnv()

    def checkEnv(self) -> None:
        # Check if Pokemon Go was requested
        self.isSourceEnabled()
        self.isDiscordOutputEnabled()

    def isSourceEnabled(self) -> None:
        res = Sources(name=self.siteName).findAllByName()
        if len(res) >= 1:
            self.sourceEnabled = True
            for i in res:
                self.links.append(i)

    def isDiscordOutputEnabled(self) -> None:
        dwh = DiscordWebHooks(name=self.siteName).findAllByName()
        if len(dwh) >= 1:
            self.outputDiscord = True
            for i in dwh:
                self.hooks.append(i)

    def getContent(self) -> str:
        try:
            
            #res: Response = get(self.uri, headers=self.getHeaders())
            #return res.content
            return self.driver.page_source
        except Exception as e:
            logger.critical(f"Failed to collect data from {self.uri}. {e}")

    def getParser(self, source: str) -> BeautifulSoup:
        try:
            return BeautifulSoup(source, features="html.parser")
        except Exception as e:
            logger.critical(f"failed to parse data returned from requests. {e}")

    def getArticles(self) -> List[Articles]:
        allArticles: List[Articles] = list()
        self.driver = self.getWebDriver()
        # Authenicate with Twitter
        appAuth = AppAuthHandler(
            consumer_key=getenv("NEWSBOT_TWITTER_API_KEY"), 
            consumer_secret=getenv("NEWSBOT_TWITTER_API_KEY_SECRET")
        )

        try:
            # auth to twitter
            api = API(appAuth)
        except Exception as e:
            logger.critical(f"Failed to authenicate with Twitter. Error: {e}")
            return allArticles

        for site in self.links:
            self.currentSite = site
            site: Sources = site
            siteSplit = site.name.split(" ")
            self.siteName = f"Twitter {siteSplit[2]}"
            siteType = siteSplit[1]
            logger.debug(f"Twitter - {siteSplit[1]} - {siteSplit[2]} - Checking for updates.")
            
            # Figure out if we are looking for a user or tag
            if siteType == "user":
                #newArticles = self.getUserTweets(api, siteSplit[2])
                #for i in newArticles:
                #    allArticles.append(i)
                pass

            elif siteType == "tag":
                for i in self.getTweets(api=api, hashtag=siteSplit[2]):
                    allArticles.append(i)

        self.__driverQuit__()
        return allArticles

    def getTweets(self, api: API, username: str = "", hashtag: str = "") -> List[Articles]:
        l = list()
        tweets = list()
        searchValue: str = ""
        if username != "":
            searchValue = f"{username}"
            for tweet in Cursor(api.user_timeline, id=username).items(30):            
                tweets.append(tweet)

        if hashtag != "":
            searchValue = hashtag
            for tweet in Cursor(api.search, q=f"#{hashtag}").items(15):
                tweets.append(tweet)

        for tweet in tweets:
            a = Articles(siteName=self.currentSite.name)
            a.description = tweet.text

            a.authorName = f"{tweet.author.name} @{tweet.author.screen_name}"
            a.authorImage = tweet.author.profile_image_url

            # Find url for the post
            a.url = self.getTweetUrl(tweet)

            try:
                tags = f'twitter, {searchValue}, '
                for t in tweet.entities['hashtags']:
                    tags += f"{t['text']}, "
                a.tags = tags
            except Exception as e:
                logger.error(f"Failed to find 'hashtags' on the tweet. \r\nError: {e}")

            try:
                a.pubDate = str(tweet.created_at)
            except Exception as e:
                logger.error(f"Failed to find 'created_at' on the tweet. \r\nError: {e}")

            # Thumbnail
            try:
                if len(tweet.entities['media']) >= 1:
                    for img in tweet.entities['media']:
                        if 'photo' in img['type'] and "twimg" in img['media_url']:
                            a.thumbnail = img['media_url']
                            break
            except:
                # I expect that this wont be found a lot, its not a problem.
                pass
            
            if a.thumbnail == '':
                try:
                    # The API does not seem to expose all images attached to the tweet.. why idk.
                    # We are going to try with Chrome to find the image.
                    # It will try a couple times to try and find the image given the results are so hit and miss.

                    self.__driverGet__(a.url)
                    source = self.getContent()
                    soup = self.getParser(source)
                    images = soup.find_all(name='img') # attrs={"alt": "Image"})
                    for img in images:
                        try:
                            # is the image in a card
                            if "card_img" in img.attrs['src']:
                                a.thumbnail = img.attrs['src']
                                break

                            if img.attrs['alt'] == 'Image':
                                a.thumbnail = img.attrs['src']
                                break
                        except:
                                pass
                except Exception as e:
                    pass

            l.append(a)

        return l

    def getTweetUrl(self, tweet: object) -> str:
        url: str = ""
        try:
            url = tweet.entities['urls'][0]['expanded_url']
        except Exception as e:
            #logger.warning(f"Failed to find the URL to the exact tweet. Checking the second location. \r\nError: {e}")
            pass

        # if the primary locacation fails, try this location
        if url == "":
            try:
                url = tweet.entities['media'][0]['expanded_url']
            except:
                #logger.error(f"Failed to find the tweet url in 'entities['media'][0]['expanded_url']")
                pass

        # if its a retweet look here
        if url == "":
            try:
                url = tweet.retweeted_status.entities['urls'][0]['expanded_url']
            except:
                pass

        if url == "":
            try:
                url = tweet.retweeted_status.entities['media'][0]['expanded_url']
            except:
                pass
        return url

    # Selenium Code
    def getWebDriver(self) -> Chrome:
        options = ChromeOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        try:
            driver = Chrome(options=options)
            return driver
        except Exception as e:
            logger.critical(f"Chrome Driver failed to start! Error: {e}")

    def __driverGet__(self, uri: str) -> None:
        try:
            self.driver.get(uri)
            #self.driver.implicitly_wait(30)
            sleep(5)
        except Exception as e:
            logger.error(f"Driver failed to get {uri}. Error: {e}")

    def __driverQuit__(self):
        self.driver.quit()

    def getImages(self, url: str) -> List[str]:
        pass
