from newsbot.sources.youtube import YoutubeReader
from newsbot.tables import Sources, DiscordWebHooks

class TestYouTube:
    def test_00EnableSource(self):
        Sources(name="Youtube LoadingReadyRun",
            url="https://www.youtube.com/user/loadingreadyrun").add()

        res = Sources(name="Youtube").findAllByName()
        if len(res) >= 1: 
            assert True 
        else: 
            assert False

    def test_01CheckSource(self):
        yt = YoutubeReader()
        assert yt.sourceEnabled

    def test_01CheckHooks(self):
        yt = YoutubeReader()
        if len(yt.hooks) == 0:
            assert True
        else: 
            assert False

    def test_01PullRss(self):
        yt = YoutubeReader()
        res = yt.getArticles()
        if len(res) >= 15:
            assert True
        else:
            assert False

    def test_02ClearSources(self):
        Sources().clearTable()
        res = Sources(name="Youtube").findAllByName()
        if len(res) == 0:
            assert True
        else:
            assert False

    def test_03EnableDiscordWebHook(self):
        DiscordWebHooks(name='Youtube LoadingReadyRun', key="invalidKey").add()
        res = DiscordWebHooks(name="Youtube").findAllByName()
        if len(res) >= 1:
            assert True
        else:
            assert False

    
