from datetime import datetime, timedelta
import json
import logging.config
import os
from pathlib import Path


"""
The following functions were used in the past but not anymore. I didn't want
to get rid of them simply because I wanted to keep them just in case.
"""


def get_latest_trading_day(current: datetime) -> str:
    """Get the lastest trading day based off of a given date. This does not account for federal holidays."""
    if current.weekday() >= 5:
        while current.weekday() >= 5:
            current -= timedelta(days=1)
        return current.strftime("%Y-%m-%d")
    elif current.weekday() == 0:
        current -= timedelta(days=3)
        return current.strftime("%Y-%m-%d")
    current -= timedelta(days=1)
    return current.strftime("%Y-%m-%d")


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
