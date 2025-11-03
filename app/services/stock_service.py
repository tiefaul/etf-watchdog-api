from dotenv import load_dotenv
from datetime import datetime
import aiohttp
from fastapi import HTTPException
from .logger_service import setup_logging
import logging

load_dotenv()

logger = logging.getLogger(__name__)
setup_logging()

class Stock:
    # Retrieve all monitored stocks
    async def get_stocks(self):
        logger.debug("Running get_stocks function...")
        stocks =  {"stocks": ["SHY", "CIBR", "IGV", "DRIV", "SPY", "SMH", "IYW"]}
        logger.info("Successfully ran get_stocks function.")
        return stocks

    # Get price for stock by date
    async def get_price_by_date(self, url: str, date: str, symbol: str, api_key: str | None):
        stock = await self.get_stocks()
        if symbol not in stock["stocks"]:
            logger.error(f"Symbol: {symbol} not in the database.", exc_info=True)
        try:
            datetime.strptime(date, "%Y-%m-%d") # Validate the date format
            # today_date = str(datetime.now().strftime("%Y-%m-%d")) # Outputs a string
        except ValueError as e:
            logger.error(f"Incorrect date format ({date}): {e}", exc_info=True)

        # Create a async request
        try:
            async with aiohttp.ClientSession() as request:
                logger.debug("Running api call to get stock price by date.")
                async with request.get(url=f'{url}/eod?symbol={symbol}&date={date}&apikey={api_key}') as response:
                    output = await response.json()
                    logger.info("Successfully ran price by date function.")
                    return output["close"]

        except KeyError as e:
            raise HTTPException(status_code=404, detail= f"{date} does not appear in the stock data: {e}")

    # Get current price of stock
    async def get_current_price(self, url: str, symbol: str, api_key: str | None):
        stock = await self.get_stocks() # Get all stocks in the database and raise an error if it doesn't exist
        if symbol not in stock["stocks"]:
            logger.error(f"Symbol: {symbol} not in the database.")

        # Create async request
        async with aiohttp.ClientSession() as request:
            logger.debug("Running api call to get current stock price.")
            async with request.get(url=f'{url}/price?symbol={symbol}&apikey={api_key}') as response:
                output = await response.json()
                logger.info("Successfully ran get current price function.")
                return output["price"]
