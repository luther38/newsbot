#import newsbot
#from newsbot.workers.pogohub import PoGoHubWorker
#from newsbot.workers.pso2 import PSO2Worker
#from newsbot.outputs.discord import Discord
#from threading import Thread

#logger = newsbot.logger
#logger.info("NewsBot has started.")

## Turn on outputs first
#oDiscord = Discord()
#tDiscord = Thread(target=oDiscord.enableThread, name="Discord")
#tDiscord.start()

#w_pogo = PoGoHubWorker()
#t_pogo = Thread(target=w_pogo.init, name="Pokemon Go Hub")
#t_pogo.start()

#w_pso2 = PSO2Worker()
#t_pso2 = Thread(target=w_pso2.init, name="PSO2")
#t_pso2.start()
