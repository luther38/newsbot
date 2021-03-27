
from newsbot.sources.rss import RssReader
from newsbot.tables import Sources

class TestRss():
    def test_00EnableSource(self):
        Sources(name="RSS Test", url="http://arstechnica.com").add()
        res = Sources(name="RSS").findAllByName()
        if len(res) >= 1:
            assert True
        