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
        stocks =  {"stocks": set(("SHY", "CIBR", "IGV", "DRIV", "SPY", "SMH", "IYW", "XLE", "AMLP", "ICLN"))}
        logger.debug("Successfully ran get_stocks function.")
        return stocks

    async def fetch_price(self, symbol: str, api_key: str):
        parameters = {"symbol": symbol, "apikey": api_key}
        session = self.get_stock_client()
        async with session.get("/price", params=parameters) as resp:
            response = await resp.json()
            price = response['price']
        return price
        # response = await req.json()
        # price = response['price']
        # return price


    # Create handler function for stock api calls
    # async def stock_data_requests(self,
    #                               symbol: str,
    #                               api_key: str,
    #                               date: str | None = None
    #                               ):
    #
    #     parameters = {"symbol": symbol, "apikey": api_key}
        # async with aiohttp.ClientSession(base_url="https://api.twelvedata.com") as request:
        #     if date:
        #         try:
        #             date_parameters = parameters.copy()
        #             date_parameters["date"] = date
        #             # Get end of day price by date
        #             logger.debug(f"Running api call to get {symbol} price by date.")
        #             async with request.get('/eod', params=date_parameters) as response:
        #                 close_date = await response.json()
        #                 logger.info(f"Successfully obtain {symbol} price on {date}.")
        #                 stock_close_date = close_date['close']
        #                 print(stock_close_date)
        #                 return stock_close_date
        #         except KeyError as e:
        #             logger.error(f"{date} does not appear in the stock data: {e}")
        #             raise HTTPException(status_code=404, detail=f"{date} does not appear in the stock data: {e}")
        #     else:
        #         logger.debug(f"Running api call to get {symbol} current stock price.")
        #         # Get the current price
        #         async with request.get('/price', params=parameters) as response:
        #             logger.info(f"Successfully obtained {symbol} current stock price.")
        #             current_price = await response.json()
        #             stock_current_price = current_price['price']
        #         logger.debug(f"Running API call to obtain {symbol} name.")
        #         async with request.get('/quote', params=parameters) as response:
        #             logger.info(f"Successfully obtained {symbol} name.")
        #             name = await response.json()
        #             stock_name = name['name']
        #             print(stock_name, stock_current_price)
        #             return stock_current_price, stock_name
