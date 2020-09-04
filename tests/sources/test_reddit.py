
from os import environ
from newsbot import env
from newsbot.initdb import InitDb
from newsbot.tables import Sources
from newsbot.sources.reddit import RedditReader

class TestReddit():
    def test_00EnableSource(self):
        environ['NEWSBOT_REDDIT_SUB_0'] = str('python')
        db = InitDb()
        #db.runMigrations()
        db.clearOldRecords()
        db.checkReddit()
        res = Sources(name='Reddit').findAllByName()
        if len(res) == 1:
            assert True
        else: assert False

    def testRssFeed(self):
        p = RedditReader()
        res = p.getArticles()
        if len(res) == 25:
            assert True
        else: assert False
