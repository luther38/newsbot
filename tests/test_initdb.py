
from newsbot.initdb import InitDb
from newsbot.db import DB, Base
from newsbot.tables import Articles, Sources
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
        