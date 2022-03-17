import json
from datetime import date
from apscheduler.schedulers.background import BlockingScheduler

def loadFile(text):
    #with open('TestSimulation.json') as test_simulation_json:
    #    data = json.load(test_simulation_json)
    #    print(data["events"])
    print(text)

time = "2022-03-17 19:34:50"
scheduler = BlockingScheduler(timezone="Europe/Berlin")
scheduler.add_job(loadFile, 'date', run_date=time, args=['text'])
scheduler.start()
