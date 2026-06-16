from fastapi import (
        APIRouter,
        Query,
        HTTPException,
        Path,
        Depends,
        )
from ..services.stock_service import StockService
from ..services.logger_service import setup_logging
from ..services.app_state import get_db_session, get_session
from ..internal.models import (
        Stock,
        StockPrice,
        StockPublic,
        StockCreate,
        )
from typing import Annotated, cast
from datetime import datetime
from dotenv import load_dotenv
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
import os
import logging
import aiohttp

load_dotenv()

twelve_data_api_key = os.getenv("TWELVE_DATA_API_KEY")
if not twelve_data_api_key:
    raise RuntimeError("The twelve_data_api_key environment variable was not set in the .env")

news_data_api_key = os.getenv("NEWS_DATA_API_KEY")
if not news_data_api_key:
    raise RuntimeError("The news_data_api_key environment variable was not set in the .env")

logger = logging.getLogger(__name__)
setup_logging()
stock = StockService()


router = APIRouter(
        prefix="/api/stocks",
        tags=["stocks"],
        responses={404: {"description": "Page Not Found"}},
        )


@router.get("/", description="List all available stocks to track.")
async def get_all_stocks(db_session: Annotated[Session, Depends(get_db_session)]):
    statement = select(Stock.ticker_symbol)
    stocks = db_session.exec(statement).all()
    if not stocks:
        raise HTTPException(status_code=404, detail="No stocks were found.")
    return {"stocks": stocks}


@router.post("/", description="Create a stock to track. Must be a real ticker symbol.", response_model=StockPublic)
async def post_stock(
        client: Annotated[aiohttp.ClientSession, Depends(get_session)],
        db_session: Annotated[Session, Depends(get_db_session)],
        symbol: StockCreate,
        ):
    try:
        stock_info = await stock.fetch_price(
                client=client,
                symbol=symbol.ticker_symbol.upper(),
                api_key=twelve_data_api_key
                )
        db_stock = Stock(
                ticker_symbol=symbol.ticker_symbol.upper(),
                company_name=stock_info["name"],
                currency="USD"
                )
        db_stock_valid = Stock.model_validate(db_stock)
        db_session.add(db_stock_valid)
        db_session.commit()
        # Add price information to the stockprice table
        db_session.add(StockPrice(
            stock_id=db_stock_valid.id, # trigger session refresh to load data from Stock object: db_stock_valid
            price_date=stock_info["date"],
            close_price=cast(float, stock_info["close_price"])
            )
        )
        db_session.commit()

        # No need to refresh the Stock object "db_stock_valid". SQLModel/SQLAlchemy already has access to all attributes
        # when we accessed db_stock_valid's id attribute in the code above. By accessing the attribute, it triggered work
        # done by SQLModel/SQLAlchemy and refreshed the data from the database (basically it ran a query to retrieve the information).
        # Calling refresh() below would be redundant here unless we need to reload updated values from the database (which was already done).
        # db_session.refresh(db_stock_valid)
        return db_stock_valid

    except aiohttp.ClientResponseError:
        raise HTTPException(status_code=404, detail="Stock could not be found. Please insure you are using the correct ticker symbol.")
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Ticker symbol already exists.")


@router.get("/{symbol}", description="Return specific ticker symbol information.")
async def get_stock(
        client: Annotated[aiohttp.ClientSession, Depends(get_session)],
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
                stock_price = await stock.fetch_price(client=client, symbol=symbol.upper(), api_key=twelve_data_api_key)
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
                raise HTTPException(status_code=404, detail=f"Price for the stock couldn't be obtained. Either the price isn't listed or API key is invalid. Symbol: {symbol}")
            except aiohttp.ClientError as e:
                logger.error(f"Network error fetching price for {symbol}: {e}")
                raise HTTPException(status_code=502, detail="Failed to connect to the external stock pricing API.")

        if date:
            try:
                # Verify date format locally to prevent invalid queries to the external API
                logger.debug("Verifying date format.")
                datetime.strptime(date, "%Y-%m-%d")
                stock_price_by_date = await stock.fetch_date(client=client, symbol=symbol.upper(), date=date, api_key=twelve_data_api_key)
                results.update({f"price_{date}": stock_price_by_date["date"]})
            except ValueError:
                # Triggered by datetime.strptime if the date string is not strictly YYYY-MM-DD
                raise HTTPException(status_code=400, detail="Invalid date format provided. Must be 'YYYY-MM-DD'.")
            except KeyError:
                # Triggered if the external API response lacks price data for the specified date (e.g., future dates, market holidays)
                raise HTTPException(status_code=404, detail=f"{date} does not appear in the stock data. Possibly tried to request data from the future or on a weekend/holiday.")
            except aiohttp.ClientError as e:
                logger.error(f"Network error fetching historical price for {symbol} on {date}: {e}")
                raise HTTPException(status_code=502, detail="Failed to connect to the external stock pricing API.")

        return results

    else:
        logger.error(f"{symbol} not found in the database.")
        raise HTTPException(status_code=404, detail=f"Symbol '{symbol}' not found in the database.")


@router.get("/{symbol}/news", description="Retrieve news articles on specific ticker symbol.")
async def get_news(client: Annotated[aiohttp.ClientSession, Depends(get_session)],
                   symbol: Annotated[str, Path(description="Get news for a stock by ticker symbol", min_length=1, max_length=5)]):
    try:
        # Calls the stock service to fetch news from the external API
        return await stock.fetch_news(client=client, symbol=symbol, api_key=news_data_api_key)
    except ValueError:
        # Handles the case where the API returns 0 results by returning a structured error message
        raise HTTPException(status_code=404, detail=f"Failed to find any news for {symbol}.")
    except aiohttp.ClientError as e:
        logger.error(f"Network error fetching news for {symbol}: {e}")
        raise HTTPException(status_code=502, detail="Failed to connect to the external news API.")
