
from typing import List
from os import environ
from newsbot.core.env import EnvRedditReader, EnvRedditDetails
import pytest

class TestEnvRedditReader():
    @pytest.fixture
    def getReader(self) -> EnvRedditReader:
        return EnvRedditReader(loadEnvFile=False)

    #@pytest.fixture
    def loadSubredditEnv(self, max:int = 1 ) -> bool:
        i:int = 0
        while i <= max:
            environ[f"NEWSBOT_REDDIT_{i}_SUBREDDIT"] = f"aww{i}"
            i = i+1
        return True

    #@pytest.fixture
    def loadDiscordLinkName(self, max:int = 1) -> bool:
        i:int = 0
        while i <= max:
            environ[f"NEWSBOT_REDDIT_{i}_LINK_DISCORD"] = f"s0.c{i}"
            i = i+1
        return True

    @pytest.mark.coreEnvReddit
    def test_loadNullEnv(self):
        r = EnvRedditReader(loadEnvFile=False)
        res = r.read()
        assert len(res) == 0

    @pytest.mark.coreEnvReddit
    def test_loadEnvOneSubreddit(self):
        self.loadSubredditEnv(max=0)
        r = EnvRedditReader(loadEnvFile=False)
        res = r.read()
        assert len(res) == 1 and res[0].subreddit == "aww0"

    @pytest.mark.coreEnvReddit
    def test_loadEnvOneSubredditInvert(self):
        self.loadSubredditEnv(max=0)
        r = EnvRedditReader(loadEnvFile=False)
        res = r.read()
        assert len(res) == 1 and res[0].subreddit != "aww1"

    @pytest.mark.coreEnvReddit
    def test_loadEnvOneDiscordLink(self):
        self.loadDiscordLinkName(max=0)
        r = EnvRedditReader(loadEnvFile=False)
        res = r.read()
        assert len(res) == 1 and res[0].discordLinkName[0] == "s0.c0"


    @pytest.mark.coreEnvReddit
    def test_loadEnvOneDiscordLinkInvert(self):
        self.loadDiscordLinkName(max=0)
        r = EnvRedditReader(loadEnvFile=False)
        res = r.read()
        assert len(res) == 1 and res[0].discordLinkName[0] != "s0.c1"

    @pytest.mark.coreEnvReddit
    def test_loadEnvOneFullEnv(self):
        self.loadSubredditEnv(max=0)
        self.loadDiscordLinkName(max=0)
        r = EnvRedditReader(loadEnvFile=False)
        res = r.read()
        assert len(res) == 1 and res[0].subreddit == 'aww0' and res[0].discordLinkName[0] == "s0.c0"
    
    @pytest.mark.coreEnvReddit
    def test_loadEnvOneFullEnvInvert(self):
        self.loadSubredditEnv(max=0)
        self.loadDiscordLinkName(max=0)
        r = EnvRedditReader(loadEnvFile=False)
        res = r.read()
        assert len(res) == 1 and res[0].subreddit != 'aww1' and res[0].discordLinkName[0] != "s0.c1"

    @pytest.mark.coreEnvReddit
    def test_loadEnvOneFullEnvInvert(self):
        self.loadSubredditEnv(max=0)
        self.loadDiscordLinkName(max=0)
        r = EnvRedditReader(loadEnvFile=False)
        res = r.read()
        assert len(res) == 1 and res[0].subreddit != 'aww1' and res[0].discordLinkName[0] != "s0.c1"
