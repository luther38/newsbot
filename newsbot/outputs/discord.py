from typing import List
from enum import Enum
import re
from time import sleep
from newsbot.env import Env
from newsbot.logger import Logger
from newsbot.sql.tables import (
    DiscordQueue,
    DiscordWebHooks,
    Icons,
    SourceLinks,
    articles,
)
from newsbot.outputs.ioutputs import IOutputs
from newsbot.common.convertHtml import ConvertHtml
from discord_webhook import DiscordWebhook, DiscordEmbed
from requests import Response


class Discord(IOutputs):
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        self.table = DiscordQueue()
        self.tempMessage: DiscordWebhook = DiscordWebhook("placeholder")
        self.env = Env()
        pass

    def enableThread(self) -> None:
        while True:
            # Tell the database to give us the queue on the table.
            try:
                queue = self.table.getQueue()

                for i in queue:

                    resp = self.sendMessage(i)

                    # Only remove the object from the queue if we sent it out correctly.
                    safeToRemove: bool = True
                    for r in resp:
                        if r.status_code != 204:
                            safeToRemove = False

                    if safeToRemove == True:
                        i.remove()

                    sleep(self.env.discord_delay_seconds)
            except Exception as e:
                self.logger.error(
                    f"Failed to post a message. {i.title}. Status_code: {resp.status_code}. msg: {resp.text}. error {e}"
                )

            sleep(self.env.discord_delay_seconds)

    def buildMessage(self, article: DiscordQueue) -> None:
        # reset the stored message
        self.tempMessage = DiscordWebhook("placeholder")

        # Extract the webhooks that relate to this site
        webhooks: List[str] = self.getHooks(
            source=article.sourceType, name=article.sourceName
        )

        # Make a new webhook with the hooks that relate to this site
        hook: DiscordWebhook = DiscordWebhook(webhooks)
        # hook.content = article.link

        title = article.title
        if len(title) >= 128:
            title = f"{title[0:128]}..."

        # Make a new Embed object
        embed: DiscordEmbed = DiscordEmbed(title=title)  # , url=article.link)

        try:
            authorIcon = self.getAuthorIcon(article.authorImage, article.siteName)
            embed.set_author(name=article.authorName, url=None, icon_url=authorIcon)
        except:
            pass

        # Discord Embed Description can only contain 2048 characters
        ch = ConvertHtml()
        if article.description != "":
            description: str = str(article.description)
            description = self.convertFromHtml(description)
            description = ch.replaceImages(description, "")
            # description = self.replaceImages(description)
            descriptionCount = len(description)
            if descriptionCount >= 2048:
                description = description[0:2040]
                description = f"{description}..."
            embed.description = description

        # Figure out if we have video based content
        if article.video != "":
            embed.description = "View the video online!"
            embed.set_video(
                url=article.video, height=article.videoHeight, width=article.videoWidth
            )

        try:
            if article.thumbnail != "":
                if " " in article.thumbnail:
                    s = article.thumbnail.split(" ")
                    embed.set_image(url=s[0])
                else:
                    embed.set_image(url=article.thumbnail)
        except Exception as e:
            self.logger.warning(
                f"Failed to attach a thumbnail. \r\n {e}\r\n thumbnails: {article.thumbnail}"
            )

        # add the link to the embed
        embed.add_embed_field(name="Link:", value=article.link)

        # Build our footer message
        footer = self.buildFooter(article.siteName)
        footerIcon = self.getFooterIcon(
            siteName=article.siteName, sourceType=article.sourceType
        )
        embed.set_footer(icon_url=footerIcon, text=footer)

        embed.set_color(color=self.getEmbedColor(article.sourceType))

        hook.add_embed(embed)
        self.tempMessage = hook

    def sendMessage(self, article: DiscordQueue) -> List[Response]:
        if article.title != "":
            self.logger.info(f"Discord - Sending article '{article.title}'")
        else:
            self.logger.info(f"Discord - Sending article '{article.description}'")
        self.buildMessage(article)
        try:
            res = self.tempMessage.execute()
        except Exception as e:
            self.logger.critical(
                f"Failed to send to Discord.  Check to ensure the webhook is correct. Error: {e}"
            )

        hooks: int = len(
            self.getHooks(source=article.sourceType, name=article.sourceName)
        )

        # Chcekcing to see if we returned a single responce or multiple.
        if hooks == 1:
            responces = list()
            responces.append(res)
        else:
            responces = res

        return responces

    def getHooks(self, source: str, name: str) -> List[str]:
        hooks = list()
        try:
            if source == "Pokemon Go Hub" or source == "Phantasy Star Online 2":
                dbHooks: SourceLinks = SourceLinks(name=f"{source}").findAllByName()
            else:
                dbHooks: SourceLinks = SourceLinks(
                    name=f"{source}_{name}"
                ).findAllByName()

            for hook in dbHooks:
                dwh = DiscordWebHooks()
                dwh.id = hook.discordID
                item: DiscordWebHooks = dwh.findById()
                if item.url != "":
                    hooks.append(item.url)
            return hooks
        except Exception as e:
            self.logger.critical(f"Unable to find DiscordWebhook for {source} {name}")

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
        msg = msg.replace("<b>", "**")
        msg = msg.replace("</b>", "**")
        msg = msg.replace("<br>", "\r\n")
        msg = msg.replace("<br/>", "\r\n")
        msg = msg.replace("\xe2\x96\xa0", "*")
        msg = msg.replace("\xa0", "\r\n")
        msg = msg.replace("<p>", "")
        msg = msg.replace("</p>", "\r\n")

        msg = self.replaceLinks(msg)
        return msg

    def replaceLinks(self, msg: str) -> str:
        """
        Find the HTML links and replace them with something discord supports.
        """
        # links = re.findall("(?<=<a )(.*)(?=</a>)", msg)
        msg = msg.replace("'", '"')
        links = re.findall("<a(.*?)a>", msg)
        for l in links:
            hrefs = re.findall('href="(.*?)"', l)
            texts = re.findall(">(.*?)</", l)
            if len(hrefs) >= 1 and len(texts) >= 1:
                discordLink = f"[{texts[0]}]({hrefs[0]})"
                msg = msg.replace(f"<a{l}a>", discordLink)
        return msg

    def replaceImages(self, msg: str) -> str:
        imgs = re.findall("<img (.*?)>", msg)
        for i in imgs:
            # Removing the images for now.
            # src = re.findall('src=(.*?)">', i)
            replace = f"<img {i}>"
            msg = msg.replace(replace, "")
        return msg

    def getAuthorIcon(self, authorIcon: str, siteName: str) -> str:
        if authorIcon != "":
            return authorIcon
        else:
            if (
                siteName == "Final Fantasy XIV"
                or siteName == "Phantasy Star Online 2"
                or siteName == "Pokemon Go Hub"
            ):
                res = Icons(site=f"Default {siteName}").findAllByName()
                return res[0].filename
            else:
                s: List[str] = siteName.split(" ")
                if s[0] == "RSS":
                    # res = Icons(site=f"Default {s[1]}").findAllByName()
                    res = Icons(site=siteName).findAllByName()
                else:
                    res = Icons(site=f"Default {s[0]}").findAllByName()
                return res[0].filename

    def buildFooter(self, siteName: str) -> str:
        footer = ""
        end: str = "Brought to you by NewsBot"
        if "reddit" in siteName.lower():
            s = siteName.split(" ")
            footer = f"{end}"
        elif "Youtube" in siteName:
            s = siteName.split(" ")
            footer = f"{s[1]} - {end}"
        elif "Instagram" in siteName or "Twitter" in siteName:
            s = siteName.split(" ")
            if s[1] == "tag":
                footer = f"#{s[2]} - {end}"
            elif s[1] == "user":
                footer = f"{s[2]} - {end}"
        elif "RSS" in siteName:
            s = siteName.split(" ")
            footer = f"{s[1]} - {end}"
        else:
            footer = end

        return footer

    def getFooterIcon(self, siteName: str, sourceType: str) -> str:
        if (
            siteName == "Phatnasy Star Online 2"
            or siteName == "Pokemon Go Hub"
            or siteName == "Final Fantasy XIV"
        ):
            res = Icons(site=f"Default {siteName}").findAllByName()
            return res[0].filename
        else:
            s: List[str] = siteName.split(" ")
            try:
                values = (f"Default {siteName}", f"Default {sourceType}", siteName)
                for v in values:
                    r = Icons(site=v).findAllByName()
                    if len(r) == 1:
                        res = r
            except:
                pass

            try:
                r = Icons(site=siteName).findAllByName()
                if len(r) == 1:
                    res = r
            except Exception as e:
                self.logger.warning(
                    f"Failed to find an icon for {siteName}. Error: {e}"
                )

            try:
                if res[0].filename != "":
                    return res[0].filename
                else:
                    return ""
            except:
                return ""

    def getEmbedColor(self, siteName: str) -> int:
        # Decimal values can be collected from https://www.spycolor.com
        if "Reddit" in siteName:
            return 16395272
        elif "Youtube" in siteName:
            return 16449542
        elif "Instagram" in siteName:
            return 13303930
        elif "Twitter" in siteName:
            return 1937134
        elif "Final Fantasy XIV" in siteName:
            return 11809847
        elif "Pokemon Go Hub" in siteName:
            return 2081673
        elif "Phantasy Star Online 2" in siteName:
            return 5557497
        elif "Twitch" in siteName:
            return 9718783
        else:
            return 0
