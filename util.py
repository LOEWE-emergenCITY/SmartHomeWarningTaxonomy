import logging
import json

file_name = 'TestSimulation.json'

def load_simulation():
    logging.info("Main    : Start loading simulation file...")
    test_simulation_json = open(file_name)
    simulation = json.load(test_simulation_json)
    logging.info("Main    : Successfully loaded simulation file")
    return simulation