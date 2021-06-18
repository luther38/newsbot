#from logging import debug
from newsbot.core.startup import CoreStartup
from newsbot.worker.startup import NewsbotWorker
from newsbot.web import start

CoreStartup().start()
NewsbotWorker().start()

#api = ApiStartup()
#apiApp = api.start()
#Thread(target=apiApp.run).start()
#apiApp.run(debug=True)
    
# Start the UI
#Thread(target=app.run(debug=True), name="WebUI").start()

#startCore()
#app = start()

