import aiohttp
from socket import AF_INET
from fastapi import HTTPException

from .logger_service import setup_logging
import logging
from typing import Optional

logger = logging.getLogger(__name__)
setup_logging()

SIZE_POOL_AIOHTTP = 100

class Stock:
    aiohttp_client: Optional[aiohttp.ClientSession] = None

    # Create startup method for Stock aiohttp client
    @classmethod
    def get_stock_client(cls) -> aiohttp.ClientSession:
        if cls.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=2)
            connector = aiohttp.TCPConnector(family=AF_INET, limit_per_host=SIZE_POOL_AIOHTTP)
            cls.aiohttp_client = aiohttp.ClientSession(base_url="https://api.twelvedata.com", timeout=timeout, connector=connector)
        return cls.aiohttp_client

    # Create shutdown method for Stock aiohttp client
    @classmethod
    async def close_stock_client(cls) -> None:
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    # Retrieve all monitored stocks
    async def get_stocks(self):
        logger.debug("Running get_stocks function...")
        stocks =  {"stocks": {"SHY", "CIBR", "IGV", "DRIV", "SPY", "SMH", "IYW", "XLE", "AMLP", "ICLN"}}
        logger.debug("Successfully ran get_stocks function.")
        return stocks

    # Get current price of stock
    async def fetch_price(self, symbol: str, api_key: str):
        parameters = {
            "symbol": symbol,
            "apikey": api_key
        }
        session = self.get_stock_client()
        async with session.get("/price", params=parameters) as resp:
            logger.debug(f"Attempting to find {symbol} current stock price.")
            response = await resp.json()
            price = response['price']
            logger.info(f"Successfully obtained {symbol} current stock price.")
        return price

    # Get stock price by a certain date
    async def fetch_date(self, symbol: str, date: str, api_key: str):
        try:
            logger.debug(f"Attempting to obtain {symbol} price by date: {date}.")
            parameters = {
                "symbol": symbol,
                "date": date,
                "apikey": api_key,
            }
            session = self.get_stock_client()
            async with session.get("/eod", params=parameters) as resp:
                response = await resp.json()
                close_date = response["close"]
                logger.info(f"Successfully obtained {symbol} price by date: {date}")
            return close_date

        except KeyError as e:
            logger.warning(f"{date} for {symbol} does not appear in the stock data: {e}")
            raise HTTPException(status_code=404, detail= f"{date} does not appear in the stock data: {e}")

# /quote for stock name


