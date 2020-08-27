from newsbot.startup import Startup

#env.newDatabase: bool = True
#env.readEnv()
#dbPath = Path("./mounts/database/newsbot.db")
#if dbPath.exists:
#    env.newDatabase = False

#system("alembic upgrade head")

s = Startup()
s.startProgram()
