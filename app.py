#from logging import debug
#from newsbotUi import start, startCore
from newsbot.web import start



# Start up core and workers
#Thread(target=Startup(), name="Core").start()

#api = ApiStartup()
#apiApp = api.start()
#Thread(target=apiApp.run).start()
#apiApp.run(debug=True)
    
# Start the UI
#Thread(target=app.run(debug=True), name="WebUI").start()

#startCore()
app = start()

