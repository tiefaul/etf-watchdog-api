from fastapi import APIRouter, Query, HTTPException, Path, Depends
from ..services.stock_service import Stock
from ..services.logger_service import setup_logging
from ..services.aiohttp_client_service import HttpClient
from typing import Annotated
from datetime import datetime
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi.logger import logger as fastAPI_logger  # convenient name
import os
import logging
import aiohttp

load_dotenv()

twelve_data_api_key = os.getenv("TWELVE_DATA_API_KEY")
news_data_api_key = os.getenv("NEWS_DATA_API_KEY")
logger = logging.getLogger(__name__)
setup_logging()
http_client = HttpClient()
stock = Stock()

@asynccontextmanager
async def lifespan(app: APIRouter):
    # Load aiohttp ClientSession
    fastAPI_logger.info("Starting aiohttp client for Stock router")
    http_client.start_http_client()
    yield
    # Shutdown aiohttp ClientSession
    fastAPI_logger.info("Closing aiohttp client for Stock router")
    await http_client.stop_http_client()

router = APIRouter(
        prefix="/api/stocks",
        tags=["stocks"],
        responses={404: {"description": "Page Not Found"}},
        lifespan=lifespan
        )

@router.get("/", description="List all available stocks to track.")
async def get_all_stocks():
    # Returns a local or cached list of stocks, avoiding unnecessary external API calls
    stocks_dict = stock.get_stocks()
    return stocks_dict

@router.get("/{symbol}")
async def get_stock(
        session: Annotated[aiohttp.ClientSession, Depends(http_client.get_session)],
        symbol: Annotated[str, Path(description="Get stock by ticker symbol.", min_length=1, max_length=5)],
        price: Annotated[bool | None, Query(description="Show current trading changes.")] = None,
        date: Annotated[str | None, Query(description="Retrieve price by date. Must be in 'year-month-day' format.")] = None
        ):
    # Validate the requested symbol against our local tracked list before querying the external API
    stock_dict = stock.get_stocks()
    if symbol.upper() in stock_dict["stocks"]:
        results = {"symbol": symbol.upper()}

        if price is True:
            try:
                stock_price = await stock.fetch_price(session=session, symbol=symbol.upper(), api_key=twelve_data_api_key)
                results.update(
                    {
                        "stock_name": stock_price["name"],
                        "price_current": stock_price["price"],
                        "date": stock_price["date"],
                        "close_price": stock_price["close_price"]
                    }
                )
            except KeyError:
                # KeyError occurs when external API returns an error payload (e.g., rate limit, invalid key) missing expected fields
                results.update({"error": f"Price for the stock couldn't be obtained. Either the price isn't listed or API key is invalid. Symbol: {symbol}"})

        if date:
            try:
                # Verify date format locally to prevent invalid queries to the external API
                logger.debug("Verifying date format.")
                datetime.strptime(date, "%Y-%m-%d")
                stock_price_by_date = await stock.fetch_date(session=session, symbol=symbol.upper(), date=date, api_key=twelve_data_api_key)
                results.update({f"price_{date}": stock_price_by_date})
            except ValueError:
                # Triggered by datetime.strptime if the date string is not strictly YYYY-MM-DD
                results.update({"error": "Invalid date provided."})
            except KeyError:
                # Triggered if the external API response lacks price data for the specified date (e.g., future dates, market holidays)
                results.update({"error": f"{date} does not appear in the stock data. Possibly tried to request data from the future 🔮"})

        return results

    else:
        logger.error(f"{symbol} not found in the database.")
        raise HTTPException(status_code=404, detail=f"Symbol '{symbol}' not found in the database.")

@router.get("/{symbol}/news")
async def get_news(session: Annotated[aiohttp.ClientSession, Depends(http_client.get_session)],
                   symbol: Annotated[str, Path(description="Get news for a stock by ticker symbol", min_length=1, max_length=5)]):
    try:
        # Calls the stock service to fetch news from the external API
        results = await stock.fetch_news(session=session, symbol=symbol, api_key=news_data_api_key)
        return results
    except ValueError:
        # Handles the case where the API returns 0 results by returning a structured error message
        # rather than throwing an HTTP exception, keeping the response consistent
        results = {"error": "Failed to find any news."}
        return results
