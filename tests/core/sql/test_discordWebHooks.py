import pytest
from os import environ, system
from newsbot.core.sql.tables import DiscordWebHooks, DiscordWebHooksTable

class TestDiscordWebHooks():
    @pytest.fixture
    def setEnv(self,):
        environ["NEWSBOT_MODE"] = 'unittest'
        system("alembic upgrade head")

    def test_add(self, setEnv):
        i = DiscordWebHooks(
            name='test',
            server='a')
        res = DiscordWebHooksTable().add(item=i)
        assert res == True