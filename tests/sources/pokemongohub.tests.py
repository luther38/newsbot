import unittest
from newsbot.sources.pokemongohub import RSSPogohub


class TestPokemonGoHub(unittest.TestCase):
    def __init__(self) -> None:
        self.site = RSSPogohub()

    def testRssFeed(self):
        # self.site.
        pass
