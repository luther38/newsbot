from typing import List

import newsbot
import re
from newsbot.outputs.outputs import Outputs
from newsbot.collections import RSSArticle, RssArticleLinks
from discord_webhook import DiscordWebhook, DiscordEmbed


class Discord(Outputs):
    def __init__(self, articles: RSSArticle) -> None:
        self.hook: DiscordWebhook = DiscordWebhook(newsbot.pogo_hook)
        self.embed: DiscordEmbed = DiscordEmbed()

        self.articles: RSSArticle = articles
        pass

    def sendMessage(self) -> None:
        self.hook.username = "Pokemon Go News"
        # self.hook.content= 'thing'

        self.embed.title = self.articles.title
        self.embed.url = self.articles.link

        # convert links
        for i in self.articles.descriptionLinks:
            discordLink: str = f"[{i.text}]({i.href})"
            self.articles.description.replace(i.raw, discordLink)

        # TODO track if we have any images in the description and if we need to handle them
        # for i in self.articles.descriptionImages:
        #    pass

        # Discord Embed Description can only contain 2048 characters
        description: str = str(self.articles.description)
        description = self.convertFromHtml(description)
        descriptionCount = len(description)
        if descriptionCount >= 2048:
            description = description[0:2040]
            description = f"{description}..."

        self.embed.description = description
        # self.embed.set_image(url=self.articles.thumbnail)

        self.hook.add_embed(self.embed)

        res = self.hook.execute()
        pass

    def convertFromHtml(self, msg: str) -> str:
        msg = msg.replace("<h2>", "**")
        msg = msg.replace("</h2>", "**")
        msg = msg.replace("<h3>", "**")
        msg = msg.replace("</h3>", "**\r\n")
        msg = msg.replace("<strong>", "**")
        msg = msg.replace("</strong>", "**\r\n")
        msg = msg.replace("<ul>", "\r\n")
        msg = msg.replace("</ul>", "")
        msg = msg.replace("</li>", "\r\n")
        msg = msg.replace("<li>", "> ")
        msg = msg.replace("&#8220;", '"')
        msg = msg.replace("&#8221;", '"')
        msg = msg.replace("&#8230;", "...")

        msg = self.replaceLinks(msg)
        return msg

    def replaceLinks(self, msg: str) -> str:
        """
        Find the HTML links and replace them with something discord supports.
        """
        # links = re.findall("(?<=<a )(.*)(?=</a>)", msg)
        links = re.findall("<a(.*?)a>", msg)
        for l in links:
            hrefs = re.findall('href="(.*?)"', l)
            texts = re.findall(">(.*?)</", l)
            discordLink = f"[{texts[0]}]({hrefs[0]})"
            msg = msg.replace(f"<a{l}a>", discordLink)
        return msg
