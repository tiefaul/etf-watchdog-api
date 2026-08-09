import logging

import aiohttp

from .logger_service import setup_logging

# Logger setup
logger = logging.getLogger(__name__)
setup_logging()

SIZE_POOL_AIOHTTP = 100
TWELVE_DATA_URL = "https://api.twelvedata.com"
NEWS_DATA_URL = "https://newsdata.io/api/1"


class StockService:
    async def fetch_quote_data(self, client: aiohttp.ClientSession, symbol: str, api_key: str | None) -> dict[str, str]:
        """
        Fetch quote data for a symbol from the Twelve Data API.

        Args:
            client (aiohttp.ClientSession): Reusable HTTP client session.
            symbol (str): The stock ticker symbol.
            api_key (str | None): The API key for Twelve Data.

        Returns:
            dict: Quote fields with keys:
                - "price": opening price from the API response.
                - "close_price": closing price converted to ``float``.
                - "date": quote timestamp.
                - "name": company name.

        Raises:
            aiohttp.ClientResponseError: If the upstream API returns a non-2xx status.
            TypeError: If ``close`` is missing and cannot be converted to ``float``.
            ValueError: If ``close`` is present but not numeric.
            KeyError: If the JSON response is empty.
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


    async def fetch_date(self, client: aiohttp.ClientSession, symbol: str, date: str, api_key: str | None) -> dict[str, float]:
        """
        Fetch end-of-day closing price for a symbol on a specific date.

        Args:
            client (aiohttp.ClientSession): Reusable HTTP client session.
            symbol (str): The stock ticker symbol.
            date (str): The date to fetch data for in 'YYYY-MM-DD' format.
            api_key (str | None): The API key for Twelve Data.

        Returns:
            dict: A dictionary containing ``{"price": <float>}``.

        Raises:
            aiohttp.ClientResponseError: If the upstream API returns a non-2xx status.
            TypeError: If ``close`` is missing and cannot be converted to ``float``.
            ValueError: If ``close`` is present but not numeric.
            KeyError: If the JSON response is empty.
        """
        logger.debug(f"Attempting to obtain {symbol} price by date: {date}.")
        parameters = {
            "symbol": symbol,
            "date": date,
            "apikey": api_key,
        }
        output: dict[str, float] = {}
        async with client.get(f"{TWELVE_DATA_URL}/eod", params=parameters) as resp:
            resp.raise_for_status()
            response = await resp.json()
            if response:
                logger.info(f"Successfully obtained {symbol} price by date: {date}")
                output["price"] = float(response.get("close"))
                return output
            raise KeyError("Error when fetching the date.")


    async def fetch_news(self, client: aiohttp.ClientSession, symbol: str, api_key: str | None) -> dict | None:
        """
        Fetch latest market news for a symbol from the NewsData.io API.

        Args:
            client (aiohttp.ClientSession): Reusable HTTP client session.
            symbol (str): The stock ticker symbol.
            api_key (str | None): The API key for authenticating with NewsData.io.

        Returns:
            dict | None: On success, returns:
                - "totalResults": number of matching items.
                - "articles": list of dictionaries with "link" and "description".
                Returns ``None`` if the API response body is empty.

        Raises:
            aiohttp.ClientResponseError: If the upstream API returns a non-2xx status.
            ValueError: If the API request succeeds but returns 0 news articles.
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
    import os

    import aiohttp
    from dotenv import load_dotenv

    load_dotenv()

    async def main():
        stock = StockService()
        api_key = os.getenv("TWELVE_DATA_API_KEY")
        async with aiohttp.ClientSession() as client:
            test = await stock.fetch_quote_data(client, "AAPL", api_key)
            print(test)
    asyncio.run(main())
