#!/usr/bin/python3

"""
This background process is meant to run on a cron or a systemd timer.
The purpose is to get all the stocks currently being tracked in the
database and update their price to the most recent closing price.
"""

import argparse
import sys
from datetime import date as date_cls
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from requests import Session


class BackgroundProcessError(Exception):
    pass


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Background process script for ETF Watchdog. This script will update the price of currently tracked stocks.")
    parser.add_argument("host", help="The domain or IP of the host for ETF Watchdog API.")
    parser.add_argument("--port", help="The port of the host", default="8000")
    parser.add_argument("--protocol", help="Network protocol. Must be https or http.", choices=["http", "https"], default="https")
    return parser.parse_args()


def session(**headers) -> Session:
    client = Session()
    if headers:
        client.headers.update(headers)
    return client


def get_stocks(client: Session, host: str) -> list[dict]:
    response = client.get(host, timeout=5)
    response.raise_for_status()
    return response.json()


def update_price(client: Session, host: str, date: str, ticker_symbol: str) -> None:
    host = host + f'{ticker_symbol}/price'
    payload = {"price_date": date}
    response = client.get(host, params=payload, timeout=5)
    response.raise_for_status()


def get_data(stock: dict) -> tuple[str, str]:
    """Retrieve ticker_symbol and date from API."""
    return stock.get("ticker_symbol", ""), stock.get("price_date", "")


def get_latest_closing_day(current) -> str:
    """Get the lastest closing day based off of a given date. This does not account for federal holidays."""
    if current.weekday() >= 5:
        while current.weekday() >= 5:
            current -= timedelta(days=1)
        return current.strftime("%Y-%m-%d")
    elif current.weekday() == 0:
        current -= timedelta(days=3)
        return current.strftime("%Y-%m-%d")
    current -= timedelta(days=1)
    return current.strftime("%Y-%m-%d")


def _convert_str_datetime(date: str) -> date_cls:
    return date_cls.fromisoformat(date)


def compare_datetime(date: str, current_date: date_cls) -> bool:
    """Compare today's date object to the one provided."""
    if not date or not isinstance(date, str):
        raise BackgroundProcessError(f"Date must a string and not empty. Date was processed as a {type(date)}")
    return _convert_str_datetime(date) == current_date


def main():
    args = parse_arguments()
    host = args.protocol + f'://{args.host}:{args.port}/api/etfs/'
    client = session()
    stocks = get_stocks(client, host)
    current_date = datetime.now(ZoneInfo("America/New_York"))
    target_closing_day = get_latest_closing_day(current_date)
    target_date = date_cls.fromisoformat(target_closing_day)
    for stock in stocks:
        try:
            symbol, date = get_data(stock)
            if compare_datetime(date, target_date):
                continue
            update_price(client, host, target_closing_day, symbol)
        except (BackgroundProcessError, ValueError) as error:
            print(error)
            continue
    client.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
