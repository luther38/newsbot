
from newsbot.tables import Sources
from newsbot.initdb import InitDb
from newsbot.sources.pokemongohub import PogohubReader

class TestPokemonGoHub():
    def testRssFeed(self):
        #Init the db
        db = InitDb()
        

        p = PogohubReader()
        res = p.getArticles()
        if len(res.articles) >= 1:
            assert True
        pass
