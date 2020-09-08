from newsbot.env import Env
from os import environ


class Test_EnvPogo:
    def test_pogoNull(self):
        e = Env()
        if e.pogo_enabled == False:
            assert True

    def test_pogoBadValue(self):
        environ["NEWSBOT_POGO_ENABLED"] = "maybe"
        e = Env()
        if e.pogo_enabled == False:
            assert True

    def test_pogoEnabledTrue(self):
        environ["NEWSBOT_POGO_ENABLED"] = "true"
        e = Env()
        if e.pogo_enabled == True:
            assert True

    def test_pogoEnabledFalse(self):
        environ["NEWSBOT_POGO_ENABLED"] = "false"
        e = Env()
        if e.pogo_enabled == False:
            assert True

    def test_webhookMissing(self):
        e = Env()

        if len(e.pogo_hooks) == 0:
            assert True

    def test_webhookEmpty(self):
        environ["NEWSBOT_POGO_HOOKS"] = ""
        e = Env()
        if len(e.pogo_hooks) == 0:
            assert True

    def test_webhook01(self):
        environ["NEWSBOT_POGO_HOOKS"] = "1"
        e = Env()
        if len(e.pogo_hooks) == 1:
            assert True

    def test_webhook02(self):
        environ["NEWSBOT_POGO_HOOKS"] = "1 2"
        e = Env()
        if len(e.pogo_hooks) == 2:
            assert True

    def test_webhook03(self):
        environ["NEWSBOT_POGO_HOOKS"] = "1 2 3"
        e = Env()
        if len(e.pogo_hooks) == 3:
            assert True


class Test_EnvPSO2:
    def test_enabledVoid(self):
        e = Env()
        if e.pso2_enabled == False:
            assert True

    def test_enabledBadValue(self):
        environ["NEWSBOT_PSO2_ENABLED"] = "maybe"
        e = Env()
        if e.pogo_enabled == False:
            assert True

    def test_EnabledTrue(self):
        environ["NEWSBOT_PSO2_ENABLED"] = "true"
        e = Env()
        if e.pogo_enabled == True:
            assert True

    def test_EnabledFalse(self):
        environ["NEWSBOT_PSO2_ENABLED"] = "false"
        e = Env()
        if e.pogo_enabled == False:
            assert True

    def test_webhookMissing(self):
        e = Env()

        if len(e.pso2_hooks) == 0:
            assert True

    def test_webhookEmpty(self):
        environ["NEWSBOT_PSO2_HOOKS"] = ""
        e = Env()
        if len(e.pso2_hooks) == 0:
            assert True

    def test_webhook01(self):
        environ["NEWSBOT_PSO2_HOOKS"] = "1"
        e = Env()
        if len(e.pso2_hooks) == 1:
            assert True

    def test_webhook02(self):
        environ["NEWSBOT_PSO2_HOOKS"] = "1 2"
        e = Env()
        if len(e.pso2_hooks) == 2:
            assert True

    def test_webhook03(self):
        environ["NEWSBOT_PSO2_HOOKS"] = "1 2 3"
        e = Env()
        if len(e.pso2_hooks) == 3:
            assert True


class Test_EnvFFXIV:
    def test_enabledAllVoid(self):
        e = Env()
        if e.ffxiv_all == False:
            assert True

    def test_enabledAllBadValue(self):
        environ["NEWSBOT_FFXIV_ALL"] = "maybe"
        e = Env()
        if e.ffxiv_all == False:
            assert True

    def test_EnabledAllTrue(self):
        environ["NEWSBOT_FFXIV_ALL"] = "true"
        e = Env()
        if e.ffxiv_all == True:
            assert True

    def test_EnabledAllFalse(self):
        environ["NEWSBOT_FFXIV_ALL"] = "false"
        e = Env()
        if e.ffxiv_all == False:
            assert True

    def test_enabledTopicsVoid(self):
        e = Env()
        if e.ffxiv_topics == False:
            assert True

    def test_enabledTopicsBadValue(self):
        environ["NEWSBOT_FFXIV_TOPICS"] = "maybe"
        e = Env()
        if e.ffxiv_topics == False:
            assert True

    def test_EnabledTopicsTrue(self):
        environ["NEWSBOT_FFXIV_TOPICS"] = "true"
        e = Env()
        if e.ffxiv_topics == True:
            assert True

    def test_EnabledTopicsFalse(self):
        environ["NEWSBOT_FFXIV_TOPICS"] = "false"
        e = Env()
        if e.ffxiv_topics == False:
            assert True

    def test_enabledNoticesVoid(self):
        e = Env()
        if e.ffxiv_notices == False:
            assert True

    def test_enabledNoticesBadValue(self):
        environ["NEWSBOT_FFXIV_NOTICES"] = "maybe"
        e = Env()
        if e.ffxiv_notices == False:
            assert True

    def test_EnabledNoticesTrue(self):
        environ["NEWSBOT_FFXIV_NOTICES"] = "true"
        e = Env()
        if e.ffxiv_notices == True:
            assert True

    def test_EnabledNoticesFalse(self):
        environ["NEWSBOT_FFXIV_NOTICES"] = "false"
        e = Env()
        if e.ffxiv_notices == False:
            assert True

    def test_enabledMaintVoid(self):
        e = Env()
        if e.ffxiv_maintenance == False:
            assert True

    def test_enabledMaintBadValue(self):
        environ["NEWSBOT_FFXIV_MAINTENANCE"] = "maybe"
        e = Env()
        if e.ffxiv_maintenance == False:
            assert True

    def test_EnabledMaintTrue(self):
        environ["NEWSBOT_FFXIV_MAINTENANCE"] = "true"
        e = Env()
        if e.ffxiv_maintenance == True:
            assert True

    def test_EnabledMaintFalse(self):
        environ["NEWSBOT_FFXIV_MAINTENANCE"] = "false"
        e = Env()
        if e.ffxiv_maintenance == False:
            assert True

    def test_enabledUpdatesVoid(self):
        e = Env()
        if e.ffxiv_updates == False:
            assert True

    def test_enabledUpdatesBadValue(self):
        environ["NEWSBOT_FFXIV_UPDATES"] = "maybe"
        e = Env()
        if e.ffxiv_updates == False:
            assert True

    def test_EnabledUpdatesTrue(self):
        environ["NEWSBOT_FFXIV_UPDATES"] = "true"
        e = Env()
        if e.ffxiv_updates == True:
            assert True

    def test_EnabledUpdatesFalse(self):
        environ["NEWSBOT_FFXIV_UPDATES"] = "false"
        e = Env()
        if e.ffxiv_updates == False:
            assert True

    def test_enabledStatusVoid(self):
        e = Env()
        if e.ffxiv_status == False:
            assert True

    def test_enabledStatusBadValue(self):
        environ["NEWSBOT_FFXIV_STATUS"] = "maybe"
        e = Env()
        if e.ffxiv_status == False:
            assert True

    def test_EnabledStatusTrue(self):
        environ["NEWSBOT_FFXIV_STATUS"] = "true"
        e = Env()
        if e.ffxiv_status == True:
            assert True

    def test_EnabledStatusFalse(self):
        environ["NEWSBOT_FFXIV_STATUS"] = "false"
        e = Env()
        if e.ffxiv_status == False:
            assert True

    def test_webhookMissing(self):
        e = Env()

        if len(e.ffxiv_hooks) == 0:
            assert True

    def test_webhookEmpty(self):
        environ["NEWSBOT_FFXIV_HOOKS"] = ""
        e = Env()
        if len(e.ffxiv_hooks) == 0:
            assert True

    def test_webhook01(self):
        environ["NEWSBOT_FFXIV_HOOKS"] = "1"
        e = Env()
        if len(e.ffxiv_hooks) == 1:
            assert True

    def test_webhook02(self):
        environ["NEWSBOT_FFXIV_HOOKS"] = "1 2"
        e = Env()
        if len(e.ffxiv_hooks) == 2:
            assert True

    def test_webhook03(self):
        environ["NEWSBOT_FFXIV_HOOKS"] = "1 2 3"
        e = Env()
        if len(e.ffxiv_hooks) == 3:
            assert True


class Test_EnvRedditSingle:
    def test_00noSubReddits(self):
        e = Env()
        if len(e.reddit_values) == 0:
            assert True

    def test_01singleSub(self):
        environ["NEWSBOT_REDDIT_SUB_0"] = str("aww")
        e = Env()
        if len(e.reddit_values) == 1 and e.reddit_values[0].site == "aww":
            assert True
        else:
            assert False

    def test_01singleHook(self):
        environ["NEWSBOT_REDDIT_HOOK_0"] = str("aww")
        e = Env()
        if len(e.reddit_values) == 1 and "aww" in e.reddit_values[0].hooks:
            assert True
        else:
            assert False

    def test_01singlBoth(self):
        environ["NEWSBOT_REDDIT_SUB_0"] = str("aww")
        environ["NEWSBOT_REDDIT_HOOK_0"] = str("aww")
        e = Env()
        if (
            len(e.reddit_values) == 1
            and "aww" in e.reddit_values[0].hooks
            and e.reddit_values[0].site == "aww"
        ):
            assert True
        else:
            assert False

    def test_02dualSub(self):
        environ["NEWSBOT_REDDIT_SUB_0"] = str("aww")
        environ["NEWSBOT_REDDIT_SUB_1"] = str("ffxiv")
        e = Env()
        if (
            len(e.reddit_values) == 2
            and e.reddit_values[0].site == "aww"
            and e.reddit_values[1].site == "ffxiv"
        ):
            assert True
        else:
            assert False

    def test_02dualhooks(self):
        environ["NEWSBOT_REDDIT_HOOK_0"] = str("pso2")
        environ["NEWSBOT_REDDIT_HOOK_1"] = str("python")
        e = Env()
        if (
            len(e.reddit_values) == 2
            and "pso2" in e.reddit_values[0].hooks
            and "python" in e.reddit_values[1].hooks
        ):
            assert True
        else:
            assert False

    def test_03combo(self):
        # environ['NEWSBOT_REDDIT_SUB_4'] = str("pso2")
        # environ['NEWSBOT_REDDIT_SUB_5'] = str("python")
        e = Env()
        if (
            len(e.reddit_values) == 2
            and e.reddit_values[0].site == "aww"
            and e.reddit_values[1].site == "ffxiv"
            and "pso2" in e.reddit_values[0].hooks
            and "python" in e.reddit_values[1].hooks
        ):
            assert True
        else:
            assert False
