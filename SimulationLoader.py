import json
from datetime import date
from multiprocessing.connection import wait
from apscheduler.schedulers.background import BlockingScheduler
from executors.optic_warning_executor import execute_optic_warning
from executors.acustic_warning_executor import execute_acustic_warning

def loadFile(file_name):
    test_simulation_json = open(file_name)
    simulation = json.load(test_simulation_json)
    return simulation

def run_simulation(simulation):
    date = simulation["config"]["date"]
    events = simulation["events"]
    scheduler = BlockingScheduler(timezone="Europe/Berlin")

    for event in events:
        execution_time = date + " " + event["time"]
        print(execution_time)
        scheduler.add_job(execute_optic_warning, 'date', run_date=execution_time, args=['fisch'])
        scheduler.add_job(execute_acustic_warning, 'date', run_date=execution_time, args=['dose'])

    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("Shutdown")
        pass

simulation = loadFile('TestSimulation.json')
run_simulation(simulation)
