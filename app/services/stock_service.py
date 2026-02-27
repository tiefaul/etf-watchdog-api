import aiohttp
from socket import AF_INET
from fastapi import HTTPException
from .logger_service import setup_logging
import logging

# Logger setup
logger = logging.getLogger(__name__)
setup_logging()

SIZE_POOL_AIOHTTP = 100

class Stock:
    aiohttp_client: aiohttp.ClientSession | None = None

    # Create startup method for Stock aiohttp client
    @classmethod
    def get_stock_client(cls):
        if cls.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=2)
            connector = aiohttp.TCPConnector(family=AF_INET, limit_per_host=SIZE_POOL_AIOHTTP)
            cls.aiohttp_client = aiohttp.ClientSession(
                base_url="https://api.twelvedata.com",
                timeout=timeout,
                connector=connector,
            )

    # Create shutdown method for Stock aiohttp client
    @classmethod
    async def close_stock_client(cls) -> None:
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    # Retrieve all monitored stocks
    async def get_stocks(self):
        logger.debug("Running get_stocks function...")
        stocks = {
            "stocks": {
                "SHY",
                "CIBR",
                "IGV",
                "DRIV",
                "SPY",
                "SMH",
                "IYW",
                "XLE",
                "AMLP",
                "ICLN",
            }
        }
        logger.debug("Successfully ran get_stocks function.")
        return stocks

    # Get current price of stock
    async def fetch_price(self, symbol: str, api_key: str | None):
        parameters = {"symbol": symbol, "apikey": api_key}
        output = {}
        async with self.aiohttp_client.get("/quote", params=parameters) as resp:
            logger.debug(f"Attempting to find {symbol} current stock price.")
            response = await resp.json()
            try:
                if response:
                    output["price"] = response["open"]
                    output["close_price"] = response["close"]
                    output["date"] = response["datetime"]
                    output["name"] = response["name"]
                else:
                    raise KeyError("Error when fetching the price data.")
            except KeyError:
                raise HTTPException(status_code=404, detail=f"Price for the stock couldn't be obtained. Either the price isn't listed or was provided an invalid stock symbol: {symbol}")
            logger.info(f"Successfully obtained {symbol} current stock price.")
        return output

    # Get stock price by a certain date
    async def fetch_date(self, symbol: str, date: str, api_key: str | None):
        try:
            logger.debug(f"Attempting to obtain {symbol} price by date: {date}.")
            parameters = {
                "symbol": symbol,
                "date": date,
                "apikey": api_key,
            }
            async with self.aiohttp_client.get("/eod", params=parameters) as resp:
                response = await resp.json()
                close_date = response["close"]
                logger.info(f"Successfully obtained {symbol} price by date: {date}")
            return close_date

        except KeyError:
            logger.warning(f"{date} for {symbol} does not appear in the stock data.")
            raise HTTPException(status_code=404, detail=f"{date} does not appear in the stock data. Possibly tried to request data from the future 🔮")
