import json
from apscheduler.schedulers.background import BlockingScheduler
from executors.optical_warning_executor import execute_optical_warning
from executors.acoustic_warning_executor import execute_acoustic_warning
from executors.email_warning_executor import execute_email_warning
from executors.sms_warning_executor import execute_sms_warning

def loadFile(file_name):
    test_simulation_json = open(file_name)
    simulation = json.load(test_simulation_json)
    return simulation

def run_simulation(simulation):
    date = simulation['config']['date']
    events = simulation['events']
    scheduler = BlockingScheduler(timezone="Europe/Berlin")

    for event in events:
        execution_time = date + " " + event['time']
        print(execution_time)
        for alert in event['alerts']:
            if alert == 'acoustic':
                scheduler.add_job(execute_acoustic_warning, 'date', run_date=execution_time, args=['acoustic'])
            if alert == 'optic':
                scheduler.add_job(execute_optical_warning, 'date', run_date=execution_time, args=['optical'])
            if alert == 'email':
                scheduler.add_job(execute_email_warning, 'date', run_date=execution_time, args=['email'])
            if alert == 'sms':
                scheduler.add_job(execute_sms_warning, 'date', run_date=execution_time, args=['sms'])

    try:
        scheduler.start()
        print('Scheduler startet')
    except KeyboardInterrupt:
        print("Shutdown")
        pass

simulation = loadFile('TestSimulation.json')
run_simulation(simulation)
#execute_email_warning('test')
