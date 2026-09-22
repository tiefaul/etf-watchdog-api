import logging

import aiohttp
from pydantic import BaseModel

from .logger_service import setup_logging

# Logger setup
logger = logging.getLogger(__name__)
setup_logging()

SIZE_POOL_AIOHTTP = 100
TWELVE_DATA_URL = "https://api.twelvedata.com"
NEWS_DATA_URL = "https://newsdata.io/api/1"


class FetchQuoteModel(BaseModel):
    price: float
    close_price: float | None = None
    date: str
    name: str


class FetchDatePriceModel(BaseModel):
    price: float


class StockService:
    async def fetch_quote_data(
        self,
        client: aiohttp.ClientSession,
        symbol: str,
        api_key: str | None,
    ) -> FetchQuoteModel:
        """
        Fetch current quote data for a symbol from Twelve Data.

        Args:
            client (aiohttp.ClientSession): Reusable HTTP client session.
            symbol (str): The stock ticker symbol.
            api_key (str | None): The API key for Twelve Data.

        Returns:
            FetchQuoteModel: Parsed quote payload with:
                - ``price`` as ``float``.
                - ``close_price`` as ``float | None``.
                - ``date`` as quote timestamp.
                - ``name`` as company name.

        Raises:
            aiohttp.ClientResponseError: If the upstream API returns a non-2xx status.
            KeyError: If the JSON response is empty.
            pydantic.ValidationError: If required fields are missing or values are invalid.
        """
        parameters = {"symbol": symbol, "apikey": api_key}

        async with client.get(f"{TWELVE_DATA_URL}/quote", params=parameters) as resp:
            logger.debug("Attempting to find %s current stock price.", symbol)
            resp.raise_for_status()
            response_data = await resp.json()

        if not response_data:
            raise KeyError("Error when fetching the price data.")

        output = FetchQuoteModel(price=response_data.get("open"),
                                 close_price=response_data.get("close"),
                                 date=response_data.get("datetime"),
                                 name=response_data.get("name"))
        logger.info("Successfully obtained %s stock price.", symbol)
        return output


    async def fetch_date(
        self,
        client: aiohttp.ClientSession,
        symbol: str,
        date: str,
        api_key: str | None,
    ) -> FetchDatePriceModel:
        """
        Fetch end-of-day closing price for a symbol on a specific date.

        Args:
            client (aiohttp.ClientSession): Reusable HTTP client session.
            symbol (str): The stock ticker symbol.
            date (str): The date to fetch data for in 'YYYY-MM-DD' format.
            api_key (str | None): The API key for Twelve Data.

        Returns:
            FetchDatePriceModel: Parsed payload with ``price`` as ``float``.

        Raises:
            aiohttp.ClientResponseError: If the upstream API returns a non-2xx status.
            KeyError: If the JSON response is empty.
            pydantic.ValidationError: If ``close`` is missing or not numeric.
        """
        logger.debug("Attempting to obtain %s price by date: %s.", symbol, date)
        parameters = {
            "symbol": symbol,
            "date": date,
            "apikey": api_key,
        }

        async with client.get(f"{TWELVE_DATA_URL}/eod", params=parameters) as resp:
            resp.raise_for_status()
            response_data = await resp.json()

        if not response_data:
            raise KeyError("Error when fetching the date.")

        logger.info("Successfully obtained %s price by date: %s", symbol, date)
        output = FetchDatePriceModel(price=response_data.get("close"))

        return output


    async def fetch_news(
        self,
        client: aiohttp.ClientSession,
        symbol: str,
        api_key: str | None,
    ) -> dict | None:
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

        async with client.get(f"{NEWS_DATA_URL}/market", params=parameters) as resp:
            resp.raise_for_status()
            response_data = await resp.json()

        if not response_data:
            return None

        logger.debug("Attempting to obtain news about %s.", symbol)
        total_results = response_data.get("totalResults") or 0
        if total_results <= 0:
            raise ValueError("News API returned 0 results.")

        articles = [
            {
                "link": article.get("link"),
                "description": article.get("description"),
            }
            for article in response_data.get("results", [])
        ]
        output = {
            "totalResults": total_results,
            "articles": articles,
        }
        logger.info("Successfully obtained news about %s.", symbol)

        return output


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
