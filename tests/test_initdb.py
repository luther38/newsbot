
from newsbot.initdb import InitDb
from newsbot.db import DB, Base
from newsbot.tables import Articles, Sources, DiscordWebHooks
from pathlib import Path
from os import remove

class Test_DB():
    def test_newDb(self):
        loc = './mounts/database/newsbot.db'
        remove(loc)
        db = DB(Base)
        new: Path = Path(loc)
        assert new.exists()

    def test_runMigrations(self):
        d = InitDb()
        d.runMigrations()
        s =Sources(name='test', url="www.python.com")
        s.add()
        res = s.findAllByName()
        assert len(res) == 1

    #def test_runDatabaseTasks(self)

class Test_Sources():
    def test_add(self):
        s = Sources(name="Source01", url="void")
        s.add()

        res = s.findAllByName()
        if res[0].name == 'Source01':
            assert True

    def test_clearTable(self):
        Sources().clearTable()
        s = Sources(name='Sources01')
        res = s.findAllByName()
        if len(res) == 0:
            assert True

class Test_DiscordWebHooks():
    def test_init00(self):
        d = DiscordWebHooks(name='test', key='url')
        if d.name == "test" and d.key == "url":
            assert True

    def test_init01(self):
        d = DiscordWebHooks(name='test')
        if d.name == 'test' and d.key == '':
            assert True

    def test_init02(self):
        d = DiscordWebHooks(key='url')
        if d.name == '' and d.key == 'url':
            assert True
    def test_init03(self):
        d = DiscordWebHooks()
        if d.name == '' and d.key == '':
            assert True

    def test_add(self):
        d = DiscordWebHooks(name="test", key='badurl').add()
        d
