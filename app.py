from newsbot.startup import Startup

# from sel import SeleniumTest
# env.newDatabase: bool = True
# env.readEnv()
# dbPath = Path("./mounts/database/newsbot.db")
# if dbPath.exists:
#    env.newDatabase = False

# system("alembic upgrade head")
# SeleniumTest().getArticles()

s = Startup()
s.startProgram()
