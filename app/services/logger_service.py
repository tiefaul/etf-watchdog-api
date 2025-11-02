import json
import logging.config
import os

# TODO: Add a logfile name param
def setup_logging():
    os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    path = os.getcwd() + "/logging_config.json"
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        raise FileNotFoundError("Cannot find the logger config. Did you change the name of the loggging config file?")
