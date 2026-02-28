import aiohttp
from socket import AF_INET
from .logger_service import setup_logging
import logging

# Logger setup
logger = logging.getLogger(__name__)
setup_logging()

SIZE_POOL_AIOHTTP = 100
TWELVE_DATA_URL = "https://api.twelvedata.com"
NEWS_DATA_URL = "https://newsdata.io/api/1"

class Stock:
    # Shared aiohttp client session used across the application lifecycle for connection pooling
    aiohttp_client: aiohttp.ClientSession | None = None

    # Create startup method for Stock aiohttp client
    @classmethod
    def get_stock_client(cls):
        # Initialize the Singleton session. Forced to IPv4 (AF_INET) and connection limited
        # to prevent port exhaustion and comply with API rate limits.
        if cls.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=2)
            connector = aiohttp.TCPConnector(family=AF_INET, limit_per_host=SIZE_POOL_AIOHTTP)
            cls.aiohttp_client = aiohttp.ClientSession(
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
        
        # Hardcoded set of allowed ETFs/Stocks to track. Acts as an initial validation 
        # layer to avoid unnecessary network calls to the external API for invalid symbols.
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
    @classmethod
    async def fetch_price(cls, symbol: str, api_key: str | None):
        parameters = {"symbol": symbol, "apikey": api_key}
        output = {}
        
        # Fetch real-time quote data. Note: Twelve Data API often returns 200 OK with an error JSON 
        # on failure (e.g., rate limit, invalid key). Accessing response["open"] will naturally raise 
        # a KeyError, which is caught and handled in the router.
        async with cls.aiohttp_client.get(f"{TWELVE_DATA_URL}/quote", params=parameters) as resp:
            logger.debug(f"Attempting to find {symbol} current stock price.")
            response = await resp.json()
            if response:
                output["price"] = response["open"]
                output["close_price"] = response["close"]
                output["date"] = response["datetime"]
                output["name"] = response["name"]
                logger.info(f"Successfully obtained {symbol} current stock price.")
                return output
            else:
                raise KeyError("Error when fetching the price data.")

    # Get stock price by a certain date
    @classmethod
    async def fetch_date(cls, symbol: str, date: str, api_key: str | None):
        logger.debug(f"Attempting to obtain {symbol} price by date: {date}.")
        parameters = {
            "symbol": symbol,
            "date": date,
            "apikey": api_key,
        }
        
        # Uses the End-Of-Day (/eod) endpoint for historical data.
        # Similar to /quote, missing data for future dates or errors will raise a KeyError.
        async with cls.aiohttp_client.get(f"{TWELVE_DATA_URL}/eod", params=parameters) as resp:
            response = await resp.json()
            if response:
                close_date = response["close"]
                logger.info(f"Successfully obtained {symbol} price by date: {date}")
                return close_date
            else:
                raise KeyError("Error when fetching the date.")

    @classmethod
    async def fetch_news(cls, symbol: str, api_key: str | None):
        parameters = {"symbol": symbol, "apikey": api_key}
        output = {"totalResults": None, "articles": []}
        async with cls.aiohttp_client.get(f"{NEWS_DATA_URL}/market", params=parameters) as resp:
            response = await resp.json()
            if response:
                output["totalResults"] = response['totalResults']
                for article in response['results']:
                    append_article = {"link": article['link'], "description": article['description']}
                    output["articles"].append(append_article)
                return output
            



