from .logger_service import setup_logging
import logging
import aiohttp
from typing import Dict, Set

# Logger setup
logger = logging.getLogger(__name__)
setup_logging()

SIZE_POOL_AIOHTTP = 100
TWELVE_DATA_URL = "https://api.twelvedata.com"
NEWS_DATA_URL = "https://newsdata.io/api/1"


class StockService:
    # Retrieve all monitored stocks
    def get_stocks(self) -> Dict[str, Set[str]]:
        """
        Retrieves the hardcoded list of valid stocks/ETFs that the application is allowed to track.
        """
        logger.debug("Running get_stocks function...")
        # Hardcoded set of allowed ETFs/Stocks to track. This is dummy data until
        # I implement an actual databse.
        return {
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


    async def fetch_price(self, client: aiohttp.ClientSession, symbol: str, api_key: str | None) -> Dict[str, str]:
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
        async with client.get(f"{TWELVE_DATA_URL}/quote", params=parameters) as resp:
            logger.debug(f"Attempting to find {symbol} current stock price.")
            resp.raise_for_status()
            response = await resp.json()
            if response:
                output["price"] = response.get("open", None) # NOTE need to do something with this.
                output["close_price"] = float(response.get("close", None))
                output["date"] = response.get("datetime", None)
                output["name"] = response.get("name", None)
                logger.info(f"Successfully obtained {symbol} stock price.")
                return output
            raise KeyError("Error when fetching the price data.")


    async def fetch_date(self, client: aiohttp.ClientSession, symbol: str, date: str, api_key: str | None) -> Dict[str, float]:
        """
        Fetches the end-of-day (EOD) historical closing price for a stock on a specific date.
        
        Args:
            symbol (str): The stock ticker symbol.
            date (str): The date to fetch data for in 'YYYY-MM-DD' format.
            api_key (str | None): The API key for Twelve Data.
            
        Returns:
            dict: Key containing The closing price for the specified date.
            
        Raises:
            KeyError: If the API returns an error or misses the expected 'close' key.
        """
        logger.debug(f"Attempting to obtain {symbol} price by date: {date}.")
        parameters = {
            "symbol": symbol,
            "date": date,
            "apikey": api_key,
        }
        output: Dict[str, float] = {}
        async with client.get(f"{TWELVE_DATA_URL}/eod", params=parameters) as resp:
            resp.raise_for_status()
            response = await resp.json()
            if response:
                logger.info(f"Successfully obtained {symbol} price by date: {date}")
                output["date"] = float(response.get("close"))
                return output
            raise KeyError("Error when fetching the date.")


    async def fetch_news(self, client: aiohttp.ClientSession, symbol: str, api_key: str | None):
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
        parameters = {"qInTitle": symbol, "apikey": api_key}
        output = {"totalResults": 0, "articles": []}
        async with client.get(f"{NEWS_DATA_URL}/market", params=parameters) as resp:
            resp.raise_for_status()
            response = await resp.json()
            if response:
                logger.debug(f"Attempting to obtain news about {symbol}.")
                if response.get('totalResults') > 0:
                    output['totalResults'] = response.get('totalResults', None)
                    # Iterate through the results and extract only the relevant fields (link and description)
                    for article in response.get('results', []):
                        append_article = {"link": article.get('link', None), "description": article.get('description', None)}
                        output["articles"].append(append_article)
                    logger.info(f"Successfully obtained news about {symbol}.")
                    return output
                raise ValueError("News API returned 0 results.")


if __name__ == "__main__":
    # For testing purposes. Run `uv run python -m backend.services.stock_service`

    import asyncio
    import aiohttp
    import os
    from dotenv import load_dotenv

    load_dotenv()

    async def main():
        stock = StockService()
        api_key = os.getenv("TWELVE_DATA_API_KEY")
        async with aiohttp.ClientSession() as client:
            test = await stock.fetch_price(client, "SPCX", api_key)
            print(test)
    asyncio.run(main())

