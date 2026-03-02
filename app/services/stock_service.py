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
        """
        Initializes the Singleton aiohttp client session for the Stock service.
        """
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
        """
        Closes the active aiohttp client session if one exists.
        """
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    # Retrieve all monitored stocks
    async def get_stocks(self):
        """
        Retrieves the hardcoded list of valid stocks/ETFs that the application is allowed to track.
        """
        logger.debug("Running get_stocks function...")
        # Hardcoded set of allowed ETFs/Stocks to track. This is dummy data until
        # I implement an actual databse.
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
        logger.info("Successfully ran get_stocks function.")
        return stocks

    # Get current price of stock
    @classmethod
    async def fetch_price(cls, symbol: str, api_key: str | None):
        """
        Fetches the current price and quote data for a given stock symbol from the Twelve Data API.
        
        Args:
            symbol (str): The stock ticker symbol.
            api_key (str | None): The API key for Twelve Data.
            
        Returns:
            dict: The current stock price, close price, date, and company name.
            
        Raises:
            KeyError: If the API returns an error or misses expected keys.
        """
        parameters = {"symbol": symbol, "apikey": api_key}
        output = {}
        # Fetch real-time quote data. Note: Twelve Data API often returns 200 OK with an error JSON 
        # on failure (e.g., rate limit, invalid key). Accessing response["open"] will naturally raise 
        # a KeyError, which is caught and handled in the router.
        async with cls.aiohttp_client.get(f"{TWELVE_DATA_URL}/quote", params=parameters) as resp:
            logger.debug(f"Attempting to find {symbol} current stock price.")
            response = await resp.json()
            if response:
                output["price"] = response.get("open")
                output["close_price"] = response.get("close")
                output["date"] = response.get("datetime")
                output["name"] = response.get("name")
                logger.info(f"Successfully obtained {symbol} current stock price.")
                return output
            else:
                raise KeyError("Error when fetching the price data.")

    # Get stock price by a certain date
    @classmethod
    async def fetch_date(cls, symbol: str, date: str, api_key: str | None):
        """
        Fetches the end-of-day (EOD) historical closing price for a stock on a specific date.
        
        Args:
            symbol (str): The stock ticker symbol.
            date (str): The date to fetch data for in 'YYYY-MM-DD' format.
            api_key (str | None): The API key for Twelve Data.
            
        Returns:
            str | float: The closing price for the specified date.
            
        Raises:
            KeyError: If the API returns an error or misses the expected 'close' key.
        """
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
                output = response["close"]
                logger.info(f"Successfully obtained {symbol} price by date: {date}")
                return output
            else:
                raise KeyError("Error when fetching the date.")

    # Get latest news for a specific stock
    @classmethod
    async def fetch_news(cls, symbol: str, api_key: str | None):
        """
        Fetches the latest news articles for a given stock symbol from the NewsData.io API.

        Args:
            symbol (str): The stock ticker symbol.
            api_key (str | None): The API key for authenticating with NewsData.io.

        Returns:
            dict: A dictionary containing the 'totalResults' and a list of 'articles'. 
                  Each article is a dictionary with 'link' and 'description' keys.

        Raises:
            ValueError: If the API request is successful but returns 0 news articles.
        """
        parameters = {"symbol": symbol, "apikey": api_key}
        output = {"totalResults": None, "articles": []}
        # Request news data using the /market endpoint of NewsData.io
        async with cls.aiohttp_client.get(f"{NEWS_DATA_URL}/market", params=parameters) as resp:
            response = await resp.json()
            if response:
                logger.debug(f"Attempting to obtain news about {symbol}.")
                # Check if the API returned any results for the symbol
                if response.get('totalResults') > 0:
                    output['totalResults'] = response['totalResults']
                    # Iterate through the results and extract only the relevant fields (link and description)
                    for article in response.get('results', []):
                        append_article = {"link": article.get('link'), "description": article.get('description')}
                        output["articles"].append(append_article)
                    logger.info(f"Successfully obtained news about {symbol}.")
                    return output
                else:
                    raise ValueError("News API returned 0 results.")
