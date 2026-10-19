from datetime import datetime, timedelta

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
