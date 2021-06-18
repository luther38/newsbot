from newsbot.core.sql.tables import Sources
from newsbot.worker.sources.reddit import RedditReader


class TestReddit:
    def test_00EnableSource(self):
        Sources(name="Reddit Python", url="https://reddit.com/r/python").add()
        res = Sources(name="Reddit").findAllByName()
        if len(res) >= 1:
            assert True
        else:
            assert False

    def testRssFeed(self):
        p = RedditReader()
        res = p.getArticles()
        if len(res) == 25:
            assert True
        else:
            assert False
