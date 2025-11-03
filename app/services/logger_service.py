import json
import logging.config
import os
from pathlib import Path

# TODO: Add a logfile name param
def setup_logging():
    new_cwd = Path(__file__).resolve().parents[2] # os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    os.chdir(new_cwd)
    path = os.getcwd() + "/logging_config.json"
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        raise FileNotFoundError("Cannot find the logger config. Did you change the name of the loggging config file?")
