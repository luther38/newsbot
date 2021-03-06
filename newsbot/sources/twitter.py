from typing import List
from newsbot import env
from newsbot.logger import Logger
from newsbot.sources.common import BChrome, ISources, BSources, UnableToFindContent, UnableToParseContent
from newsbot.tables import Articles, Sources, DiscordWebHooks
from requests import get, Response
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
from tweepy import AppAuthHandler, API, Cursor
from os import getenv
from time import sleep


class TwitterReader(ISources, BSources, BChrome):
    def __init__(self):
        self.logger = Logger(__class__)
        self.uri: str = "https://twitter.com"
        self.baseUri = self.uri
        self.siteName: str = "Twitter"

        self.links: List[Sources] = list()
        self.hooks: List[DiscordWebHooks] = list()

        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False
        self.checkEnv(self.siteName)

    def getArticles(self) -> List[Articles]:
        allArticles: List[Articles] = list()
        self.driver = self.driverStart()
        # Authenicate with Twitter
        appAuth = AppAuthHandler(
            consumer_key=getenv("NEWSBOT_TWITTER_API_KEY"),
            consumer_secret=getenv("NEWSBOT_TWITTER_API_KEY_SECRET"),
        )

        try:
            # auth to twitter
            api = API(appAuth)
        except Exception as e:
            self.logger.critical(f"Failed to authenicate with Twitter. Error: {e}")
            return allArticles

        for site in self.links:
            self.currentSite = site
            site: Sources = site
            siteSplit = site.name.split(" ")
            self.siteName = f"Twitter {siteSplit[2]}"
            siteType = siteSplit[1]
            self.logger.debug(
                f"Twitter - {siteSplit[1]} - {siteSplit[2]} - Checking for updates."
            )

            # Figure out if we are looking for a user or tag
            if siteType == "user":
                for i in self.getTweets(api, siteSplit[2]):
                    allArticles.append(i)

            elif siteType == "tag":
                for i in self.getTweets(api=api, hashtag=siteSplit[2]):
                    allArticles.append(i)

        self.driverClose()
        return allArticles

    def getTweets(
        self, api: API, username: str = "", hashtag: str = ""
        ) -> List[Articles]:

        l = list()
        tweets = list()
        searchValue: str = ""
        if username != "":
            searchValue = f"{username}"
            for tweet in Cursor(api.user_timeline, id=username).items(15):
                tweets.append(tweet)

        if hashtag != "":
            searchValue = hashtag
            for tweet in Cursor(api.search, q=f"#{hashtag}").items(15):
                tweets.append(tweet)

        for tweet in tweets:

            # Ignore retweets?
            if tweet.in_reply_to_screen_name != None:
                continue

            a = Articles(siteName=self.currentSite.name)
            a.description = tweet.text

            a.authorName = f"{tweet.author.name} @{tweet.author.screen_name}"
            a.authorImage = tweet.author.profile_image_url

            # Find url for the post
            a.url = f"https://twitter.com/{tweet.author.screen_name}/status/{tweet.id}"
            # a.url = self.getTweetUrl(tweet)

            if a.exists() == False:
                try:
                    tags = f"twitter, {searchValue}, "
                    for t in tweet.entities["hashtags"]:
                        tags += f"{t['text']}, "
                    a.tags = tags
                except Exception as e:
                    self.logger.error(f"Failed to find 'hashtags' on the tweet. \r\nError: {e}")

                try:
                    a.pubDate = str(tweet.created_at)
                except Exception as e:
                    self.logger.error(
                        f"Failed to find 'created_at' on the tweet. \r\nError: {e}"
                    )

                # Thumbnail
                try:
                    if len(tweet.entities["media"]) >= 1:
                        for img in tweet.entities["media"]:
                            if "photo" in img["type"] and "twimg" in img["media_url"]:
                                a.thumbnail = img["media_url"]
                                break
                except:
                    # I expect that this wont be found a lot, its not a problem.
                    pass

                if a.thumbnail == "":
                    try:
                        # The API does not seem to expose all images attached to the tweet.. why idk.
                        # We are going to try with Chrome to find the image.
                        # It will try a couple times to try and find the image given the results are so hit and miss.
                        album: str = ""
                        self.driverGoTo(a.url)
                        source = self.getDriverContent()
                        soup = self.getParser(seleniumContent=source)
                        images = soup.find_all(name="img")  # attrs={"alt": "Image"})
                        for img in images:
                            try:
                                # is the image in a card
                                if "card_img" in img.attrs["src"]:
                                    a.thumbnail = img.attrs["src"]
                                    break

                                if img.attrs["alt"] == "Image":
                                    album += f"{img.attrs['src']} "
                                    # a.thumbnail = img.attrs['src']
                                    # break
                            except Exception as e:
                                pass

                        # take all the images found, and flatten the list to a str for storage
                        a.thumbnail = album
                    except Exception as e:
                        pass

                l.append(a)

        return l

    def getTweetUrl(self, tweet: object) -> str:
        url: str = ""
        try:
            url = tweet.entities["urls"][0]["expanded_url"]
        except:
            # self.logger.warning(f"Failed to find the URL to the exact tweet. Checking the second location. \r\nError: {e}")
            pass

        # if the primary locacation fails, try this location
        if url == "":
            try:
                url = tweet.entities["media"][0]["expanded_url"]
            except:
                # self.logger.error(f"Failed to find the tweet url in 'entities['media'][0]['expanded_url']")
                pass

        # if its a retweet look here
        if url == "":
            try:
                url = tweet.retweeted_status.entities["urls"][0]["expanded_url"]
            except:
                pass

        if url == "":
            try:
                url = tweet.retweeted_status.entities["media"][0]["expanded_url"]
            except:
                pass
        return url



    def getImages(self, url: str) -> List[str]:
        pass
