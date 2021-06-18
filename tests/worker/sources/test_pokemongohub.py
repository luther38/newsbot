from newsbot.core.sql.tables import Sources, DiscordWebHooks, Articles
from newsbot.worker.sources.pokemongohub import PogohubReader


class TestPokemonGoHub:
    def test_00EnableSource(self):
        # environ["NEWSBOT_POGO_ENABLED"] = str("true")
        Sources(name="Pokemon Go Hub", url="https://pokemongohub.net/rss").add()
        res = Sources(name="Pokemon Go Hub").findAllByName()
        if len(res) >= 1:
            assert True
        else:
            assert False

    def test_01GetEnabled(self):
        pgh = PogohubReader()
        assert pgh.sourceEnabled

    def test_01GetHooks(self):
        pgh = PogohubReader()
        if len(pgh.hooks) == 0:
            assert True
        else:
            assert False

    def test_01PullRssFeed(self):
        p = PogohubReader()
        res = p.getArticles()
        if len(res) == 30:
            assert True
        else:
            assert False

    def test_02ItemTitle(self):
        # All articles need to have a title
        r = PogohubReader()
        res = r.getArticles()
        for i in res:
            i: Articles = i
            if i.title == "":
                assert False

        assert True

    def test_02ItemTags(self):
        # All articles need to have tags
        r = PogohubReader()
        res = r.getArticles()
        for i in res:
            i: Articles = i
            if i.tags == "":
                assert False

        assert True

    def test_02ItemUrl(self):
        # All articles need to have a url
        r = PogohubReader()
        res = r.getArticles()
        for i in res:
            i: Articles = i
            if i.url == "":
                assert False

        assert True

    def test_02ItemPubDate(self):
        # All articles need to have tags
        r = PogohubReader()
        res = r.getArticles()
        for i in res:
            i: Articles = i
            if i.pubDate == "":
                assert False

        assert True
