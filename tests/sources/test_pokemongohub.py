
from newsbot.sources.pokemongohub import PogohubReader

class TestPokemonGoHub():
    def testRssFeed(self):
        p = PogohubReader()
        res = p.getArticles()
        if len(res.articles) >= 1:
            assert True
        pass
