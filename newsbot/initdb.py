
from os import system
from newsbot import env
from newsbot.tables import Sources, DiscordWebHooks

class InitDb():
    def __init__(self) -> None:
        #self.runMigrations()
        #self.clearOldRecords()
        #self.runDatabaseTasks()
        pass

    def runMigrations(self) -> None:
        system("alembic upgrade head")

    def clearOldRecords(self) -> None:
        #clear our the table cache from last startup
        Sources().clearTable()
        DiscordWebHooks().clearTable()

    def runDatabaseTasks(self):

        #Inject new values based off env values
        # if the user did not request a source, we will ignore it.
        if env.pogo_enabled == True:
            # Pokemon Go Hub only has one source
            Sources(name="Pokemon Go Hub", url="https://pokemongohub.net/rss").add()
            #Sources(name="Pokemon Go Hub", url="https://pokemongohub.net/post/category/news/").add()
            for i in env.pogo_hooks:
                DiscordWebHooks(name="Pokemon Go Hub", key=i).add()

        if env.pso2_enabled == True:
            Sources(name="Phantasy Star Online 2", url="https://pso2.com/news").add()
            for i in env.pso2_hooks:
                DiscordWebHooks(name="Phantasy Star Online 2", key=i).add()

        if env.ffxiv_all == True or env.ffxiv_topics == True:
            Sources(name="Final Fantasy XIV Topics", url="https://na.finalfantasyxiv.com/lodestone/topics/").add()
        
        if env.ffxiv_all == True or env.ffxiv_notices == True:
            Sources(name="Final Fantasy XIV Notices", url='https://na.finalfantasyxiv.com/lodestone/news/category/1').add()
            
        if env.ffxiv_all == True or env.ffxiv_maintenance == True:
            Sources(name="Final Fantasy XIV Maintenance", url='https://na.finalfantasyxiv.com/lodestone/news/category/2').add()
            
        if env.ffxiv_all == True or env.ffxiv_updates == True:
            Sources(name="Final Fantasy XIV Updates", url='https://na.finalfantasyxiv.com/lodestone/news/category/3').add()

        if env.ffxiv_all == True or env.ffxiv_status == True:
            Sources(name="Final Fantasy XIV Status", url='https://na.finalfantasyxiv.com/lodestone/news/category/4').add()
 
        for i in env.ffxiv_hooks:
            DiscordWebHooks(name="Final Fantasy XIV", key=i).add()

        for i in env.reddit_values:
            r1 = f"Reddit {i.site}"
            Sources(name=r1, url=f"https://reddit.com/r/{i.site}").add()
            for h in i.hooks:
                DiscordWebHooks(name=r1, key=h).add()
