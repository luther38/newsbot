from newsbot.tables import Sources
from newsbot.initdb import InitDb
from newsbot.env import Env
from os import environ
from newsbot.sources.pokemongohub import PogohubReader

class TestPokemonGoHub():
    def test_00EnableSource(self):
        environ['NEWSBOT_POGO_ENABLED'] = str('true')
        e = Env()
        db = InitDb()
        db.runMigrations()
        db.clearOldRecords()
        db.checkPokemonGoHub()
        res = Sources(name='Pokemon Go Hub').findAllByName()
        if len(res) == 1:
            assert True
        else: assert False

    def testRssFeed(self):
        p = PogohubReader()
        res = p.getArticles()
        if len(res) == 30:
            assert True
        else: assert False
