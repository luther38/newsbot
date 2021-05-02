from logging import debug
from threading import Thread
from newsbot.core.startup import Startup
from newsbot.worker.startup import NewsbotWorker
from newsbotUi import app

# Start up core and workers
#Thread(target=Startup(), name="Core").start()
coreStarted: bool = False
workerStarted: bool = False
uiStarted: bool = False

if coreStarted == False:
    Startup()
    coreStarted = True
if workerStarted == False:
    NewsbotWorker()
    workerStarted = True

# Start the UI
#Thread(target=app.run(debug=True), name="WebUI").start()
if uiStarted == False:
    #app.run(debug=True)
    uiStarted = True


