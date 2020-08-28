from newsbot.initdb import InitDb
from newsbot.db import DB, Base
from newsbot.tables import Articles, Sources, DiscordWebHooks
from pathlib import Path
from os import remove


class Test_DB:
    def test_newDb(self):
        loc = "./mounts/database/newsbot.db"
        remove(loc)
        db = DB(Base)
        new: Path = Path(loc)
        assert new.exists()

    def test_runMigrations(self):
        d = InitDb()
        d.runMigrations()
        s = Sources(name="test", url="www.python.com")
        s.add()
        res = s.findAllByName()
        assert len(res) == 1

    # def test_runDatabaseTasks(self)


class Test_Sources:

    def test_init00(self):
        s = Sources()
        if s.name == '' and s.url == '':
            assert True

    def test_init01(self):
        s = Sources(name="init01")
        if s.name == "init01" and s.url == '':
            assert True

    def test_init02(self):
        s = Sources(url='init02')
        if s.name == '' and s.url == 'init02':
            assert True

    def test_add(self):
        s = Sources(name="Source01", url="void")
        s.add()

        res = s.findAllByName()
        if res[0].name == "Source01":
            assert True
    
    def test_add01(self):
        s = Sources(name="", url="void")
        s.add()

        res = s.findAllByName()
        if res[0].name == "" and res[0].url == 'void':
            assert True

    def test_clearTable(self):
        Sources().clearTable()
        s = Sources(name="Sources01")
        res = s.findAllByName()
        if len(res) == 0:
            assert True

class Test_DiscordWebHooks:
    def test_init00(self):
        d = DiscordWebHooks(name="test", key="url")
        if d.name == "test" and d.key == "url":
            assert True

    def test_init01(self):
        d = DiscordWebHooks(name="test")
        if d.name == "test" and d.key == "":
            assert True

    def test_init02(self):
        d = DiscordWebHooks(key="url")
        if d.name == "" and d.key == "url":
            assert True

    def test_init03(self):
        d = DiscordWebHooks()
        if d.name == "" and d.key == "":
            assert True

    def test_add(self):
        try:
            DiscordWebHooks(name="test", key="badurl").add()
            assert True
        except:
            assert False

    def test_clearTable(self):
        DiscordWebHooks().clearTable()
        res = len(DiscordWebHooks())
        if res == 0:
            assert True
