import datetime
import time
from util import load_simulation

def setup_scheduler():
    simulation = load_simulation()
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    date = simulation['config']['date']
    events = simulation['events']

    while len(events) != 0:
        for event in events:
            time_event = date + event['time']
            if (time_event == time_now):
                print("Event executed")
                print(event['message'])
        time.sleep(60)
            


print(datetime.datetime.now())
setup_scheduler()