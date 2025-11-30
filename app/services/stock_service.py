from datetime import datetime
import aiohttp
from fastapi import HTTPException
from .logger_service import setup_logging
import logging

logger = logging.getLogger(__name__)
setup_logging()

class Stock:
    # Create handler function for stock api calls
    async def stock_data_requests(self, symbol: str, date: str | None = None, api_key: str | None = None):
            async with aiohttp.ClientSession(base_url="https://api.twelvedata.com") as request:
                parameters = {"symbol": symbol, "apikey": api_key}
                if date:
                    parameters["date"] = date
                    logger.debug(f"Running api call to get {symbol} price by date.")

                    try:
                        async with request.get('/eod', params=parameters) as response:
                            close_date = await response.json()
                            logger.info(f"Successfully obtain {symbol} price on {date}.")
                            return close_date['close']
                    except KeyError as e:
                        raise HTTPException(status_code=404, detail=f"{date} does not appear in the stock data: {e}")

                logger.debug(f"Running api call to get {symbol} current stock price.")
                async with request.get('/price', params=parameters) as response:
                    logger.info(f"Successfully obtained {symbol} current stock price.")
                    current_price = await response.json()
                    return current_price['price']

    # Retrieve all monitored stocks
    async def get_stocks(self):
        logger.debug("Running get_stocks function...")
        stocks =  {"stocks": set(("SHY", "CIBR", "IGV", "DRIV", "SPY", "SMH", "IYW", "XLE", "AMLP", "ICLN"))}
        logger.info("Successfully ran get_stocks function.")
        return stocks

    # Get price for stock by date
    async def get_price_by_date(self, date: str, symbol: str, api_key: str | None):
        # Get all stocks in the database and raise an error if symbol does not exist
        stock = await self.get_stocks()
        if symbol not in stock["stocks"]:
            logger.error(f"Symbol: {symbol} not in the database.")
        try:
            # Validate date format
            datetime.strptime(date, "%Y-%m-%d")
            # today_date = str(datetime.now().strftime("%Y-%m-%d")) # Outputs a string
        except ValueError as e:
            logger.error(f"Incorrect date format ({date}): {e}", exc_info=True)

        # Make request to the api
        logger.debug("Running api call to get stock price by date.")
        output = await self.stock_data_requests(symbol=symbol, date=date, api_key=api_key)
        logger.debug("Successfully ran get_price_by_date function.")
        return output

    # Get current price of stock
    async def get_current_price(self, symbol: str, api_key: str | None):
        # Get all stocks in the database and raise an error if symbol does not doesn't exist
        stock = await self.get_stocks()
        if symbol not in stock["stocks"]:
            logger.error(f"Symbol: {symbol} not in the database.")

        # Make request to the api
        logger.debug("Running api call to get current stock price.")
        output = await self.stock_data_requests(symbol=symbol, api_key=api_key)
        logger.debug("Successfully ran get_current_price function.")
        return output

    async def get_news(self,):
        pass
