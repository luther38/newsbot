from newsbot.logger import Logger
from os import getenv
from requests import post, get
from json import loads, JSONEncoder
from typing import Dict, List, NamedTuple


class TwitchAuth:
    def __init__(
        self,
        access_token: str = "",
        expires_in: int = 0,
        token_type: str = "",
        client_id: str = "",
    ):
        self.access_token = access_token
        self.expires_in = expires_in
        self.token_type = token_type
        self.client_id = client_id
        pass


class TwitchChannel:
    ## might go away
    def __init__(self, obj: Dict = {}):
        self.broadcaster_language: str = obj.get("broadcaster_language")
        self.display_name: str = obj.get("display_name")
        self.game_id: int = int(obj.get("game_id"))
        self.id: int = int(obj.get("id"))
        self.is_live: bool = bool(obj.get("is_live"))
        self.tag_ids: List[str] = obj.get("tag_ids")
        self.thumbnail_url: str = str(obj.get("thumbnail_url"))
        self.title: str = str(obj.get("title"))
        self.started_at: str = str(obj.get("started_at"))
        self.game_data = TwitchGameData()


class TwitchUser:
    def __init__(self, obj: Dict):
        self.id = obj.get("id")
        self.login = obj.get("login")
        self.display_name = obj.get("display_name")
        self.type = obj.get("type")
        self.broadcaster_type = obj.get("broadcaster_type")
        self.description = obj.get("description")
        self.profile_image_url = obj.get("profile_image_url")
        self.offline_image_url = obj.get("offline_image_url")
        self.view_count = obj.get("view_count")


class TwitchVideo:
    def __init__(self, obj: Dict):
        self.id = obj.get("id")
        self.user_id = obj.get("user_id")
        self.user_name = obj.get("user_name")
        self.title = obj.get("title")
        self.description = obj.get("description")
        self.created_at = obj.get("created_at")
        self.published_at = obj.get("published_at")
        self.url = obj.get("url")
        self.thumbnail_url = obj.get("thumbnail_url")
        self.viewable = obj.get("viewable")
        self.view_count = obj.get("view_count")
        self.language = obj.get("language")
        self.type = obj.get("type")
        self.duration = obj.get("duration")
        pass


class TwitchClip:
    def __init__(self, obj: Dict = {}):
        self.id = obj.get("id")
        self.url = obj.get("url")
        self.embed_url = obj.get("embed_url")
        self.broadcaster_id = obj.get("broadcaster_id")
        self.broadcaster_name = obj.get("broadcaster_name")
        self.creator_id = obj.get("creator_id")
        self.creator_name = obj.get("creator_name")
        self.video_id = obj.get("video_id")
        self.game_id = obj.get("game_id")
        self.language = obj.get("language")
        self.title = obj.get("title")
        self.view_count = obj.get("view_count")
        self.created_at = obj.get("created_at")
        self.thumbnail_url = obj.get("thumbnail_url")
        pass


class TwitchGameData:
    def __init__(self, obj: Dict = {}):
        self.id = 0
        try:
            self.id = int(obj.get("id"))
        except:
            pass

        self.name: str = obj.get("name")
        self.box_art_url: str = obj.get("box_art_url")
        pass


class TwitchStream:
    def __init__(self, obj: Dict = {}):
        self.id = obj.get("id")
        self.user_id = obj.get("user_id")
        self.user_name = obj.get("user_name")
        self.game_id = obj.get("game_id")
        self.type = obj.get("type")
        self.title = obj.get("title")
        self.viewer_count = obj.get("viewer_count")
        self.started_at = obj.get("started_at")
        self.language = obj.get("language")
        self.thumbnail_url = obj.get("thumbnail_url")
        self.tags_ids = obj.get("tag_ids")


class TwitchAPI:
    def __init__(self):
        self.uri: str = "https://id.twitch.tv"
        self.apiUri: str = "https://api.twitch.tv/helix"
        pass

    def auth(self) -> TwitchAuth:
        """
        https://dev.twitch.tv/docs/authentication/getting-tokens-oauth#oauth-client-credentials-flow
        """
        client_id = str(getenv("NEWSBOT_TWITCH_CLIENT_ID"))
        client_secret = str(getenv("NEWSBOT_TWITCH_CLIENT_SECRET"))
        scopes = "user:read:email"
        uri = f"https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials&scopes={scopes}"

        res = post(uri)
        if res.status_code != 200:
            Logger().error(res.text)
            return TwitchAuth()
        else:
            token = loads(res.content)
            o = TwitchAuth(
                access_token=token["access_token"],
                expires_in=token["expires_in"],
                token_type=token["token_type"],
                client_id=client_id,
            )
            return o

    def getUser(self, auth: TwitchAuth, username: str) -> None:
        uri = f"{self.apiUri}/users?login={username}"
        res = get(uri, headers=self.__header__(auth))
        if res.status_code != 200:
            Logger().error(
                f"Failed to get user information. StatusCode: {res.status_code}, Error: {res.text}"
            )
        else:
            json = loads(res.content)
            if len(json["data"]) == 1:
                user = TwitchUser(json["data"][0])
            else:
                Logger().error(f"Did not get a usable object.")
                user = TwitchUser({})
            return user

    def searchForUser(self, auth: TwitchAuth, username: str = "") -> None:
        if username == "":
            Logger().error(
                f"Request to search for user was requested but no user was given."
            )
        else:
            uri: str = f"{self.apiUri}/search/channels?query={username}"
            header = self.__header__(auth)
            res = get(uri, headers=header)
            if res.status_code != 200:
                Logger().error(
                    f"Attempted to pull user information but failed. status_code: {res.status_code}, output: {res.text}"
                )
            else:
                l = list()
                j = loads(res.content)
                for i in j["data"]:
                    # Convert the Json date to an object
                    stream = TwitchChannel(i)
                    # Get the game details
                    # stream.game_data = self.getGame(auth,stream.game_id)
                    # video = self.getVideos(auth=auth, user_id=stream.id)
                    l.append(stream)
                return l

    def getGame(self, auth: TwitchAuth, game_id: int) -> TwitchGameData:
        uri = f"{self.apiUri}/games?id={game_id}"
        headers = self.__header__(auth)
        res = get(uri, headers=headers)

        if res.status_code != 200:
            Logger().error(
                f"Attempted to get Twich Game data but failed on game_id: {game_id}. output: {res.text}"
            )
            return TwitchGameData()
        else:
            j = loads(res.content)
            if len(j["data"]) != 0:
                game = TwitchGameData(j["data"][0])
            else:
                game = TwitchGameData()
            return game

    def getVideos(
        self, auth: TwitchAuth, id: int = 0, user_id: int = 0, game_id: int = 0
    ) -> List[TwitchVideo]:
        uri = f"{self.apiUri}/videos"
        if id != 0:
            uri = f"{uri}?id={id}"
        elif user_id != 0:
            uri = f"{uri}?user_id={user_id}"
        elif game_id != 0:
            uri = f"{uri}?game_id={game_id}"

        res = get(uri, headers=self.__header__(auth))
        videos = list()
        if res.status_code != 200:
            Logger().error(f"Failed to request videos")
            return videos
        else:
            json = loads(res.content)
            for i in json["data"]:
                videos.append(TwitchVideo(i))
            return videos

    def getClips(
        self, auth: TwitchAuth, user_id: int = 0, clip_id: str = "", game_id: int = 0
    ) -> List[TwitchClip]:
        uri = f"{self.apiUri}/clips"
        if user_id != 0:
            uri = f"{uri}?broadcaster_id={user_id}"
        elif clip_id != "":
            uri = f"{uri}?id={clip_id}"
        elif game_id != 0:
            uri = f"{uri}?game_id={game_id}"
        else:
            Logger().error(
                f"Clips was requested but was given invalid parameters, returning empty object."
            )
            return ""

        res = get(uri, headers=self.__header__(auth))
        clips = list()
        if res.status_code != 200:
            Logger().error(
                f"Clips request returnd a bad status_code. Code: {res.status_code}, Error: {res.text}"
            )
            return clips
        else:
            json = loads(res.content)
            for i in json["data"]:
                clips.append(TwitchClip(i))

        return clips

    def getStreams(
        self, auth: TwitchAuth, game_id: int = 0, user_id: int = 0, user_login: str = ""
    ) -> None:
        uri = f"{self.apiUri}/streams"
        if game_id != 0:
            uri = f"{uri}?game_id={game_id}"
        elif user_id != 0:
            uri = f"{uri}?user_id={user_id}"
        elif user_login != "":
            uri = f"{uri}?user_login={user_login}"
        else:
            pass

        res = get(uri, headers=self.__header__(auth))
        streams = list()
        if res.status_code != 200:
            Logger().error(
                f"Streams request returned a bad status_code. Code: {res.status_code}, Error: {res.test}"
            )
            return streams
        else:
            json = loads(res.content)
            if len(json["data"]) == 0:
                streams.append(TwitchStream())
            for i in json["data"]:
                streams.append(TwitchStream(i))

        return streams

    def __header__(self, auth: TwitchAuth) -> Dict:
        return {
            "Authorization": f"Bearer {auth.access_token}",
            "Client-ID": f"{auth.client_id}",
        }
