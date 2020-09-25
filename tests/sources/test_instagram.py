from newsbot.sources.instagram import InstagramReader
from newsbot.tables import Sources, DiscordWebHooks, Articles


class TestInstagram:
    def test_00EnableSource(self):
        Sources(name="Instagram tag pokemongo", url="pokemongo").add()

        res = Sources(name="Instagram").findAllByName()
        if len(res) >= 1:
            assert True
        else:
            assert False

    def test_01CheckSource(self):
        ig = InstagramReader()
        assert ig.sourceEnabled

    def test_01CheckDiscord(self):
        ig = InstagramReader()
        if len(ig.hooks) == 0:
            assert True
        else:
            assert False

    def test_02PullFeed(self):
        ig = InstagramReader()
        res = ig.getArticles()
        if len(res) >= 9:
            assert True
        else:
            assert False

    def test_02ItemTitle(self):
        # All articles need to have a title
        ig = InstagramReader()
        res = ig.getArticles()
        for i in res:
            i: Articles = i
            if i.title == "":
                assert False

        assert True

    def test_02ItemTags(self):
        # All articles need to have tags
        ig = InstagramReader()
        res = ig.getArticles()
        for i in res:
            i: Articles = i
            if i.tags == "":
                assert False

        assert True

    def test_02ItemUrl(self):
        # All articles need to have tags
        ig = InstagramReader()
        res = ig.getArticles()
        for i in res:
            i: Articles = i
            if i.url == "":
                assert False

        assert True

    def test_02ItemPubDate(self):
        # All articles need to have tags
        ig = InstagramReader()
        res = ig.getArticles()
        for i in res:
            i: Articles = i
            if i.pubDate == "":
                assert False

        assert True
