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
        StockPublic,
        StockCreate,
        StockPrice,
        StockPricePublic
        )
from typing import Annotated, List, cast, Dict
from datetime import date, timedelta
from dotenv import load_dotenv
from sqlmodel import Session, select, col
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
import os
import logging
import aiohttp

load_dotenv()

TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")
if not TWELVE_DATA_API_KEY:
    raise RuntimeError("The TWELVE_DATA_API_KEY environment variable was not set in the .env")

NEWS_DATA_API_KEY = os.getenv("NEWS_DATA_API_KEY")
if not NEWS_DATA_API_KEY:
    raise RuntimeError("The NEWS_DATA_API_KEY environment variable was not set in the .env")

logger = logging.getLogger(__name__)
setup_logging()
stock = StockService()


router = APIRouter(
        prefix="/api/etfs",
        tags=["etfs"],
        responses={404: {"description": "Page Not Found"}},
        )


def get_latest_trading_day(current: date) -> date:
    while current.weekday() >= 5:
        current -= timedelta(days=1)
    return current


@router.get("/", description="List all available stocks to track.", response_model=List[str])
async def get_all_stocks(db_session: Annotated[Session, Depends(get_db_session)]):
    statement = select(Stock.ticker_symbol)
    stocks = db_session.exec(statement).all()
    if not stocks:
        raise HTTPException(status_code=404, detail="No stocks found in the database.")
    return stocks


@router.post("/", description="Create a stock to track. Must be a real ticker symbol.", response_model=StockPublic)
async def post_stock(
        client: Annotated[aiohttp.ClientSession, Depends(get_session)],
        db_session: Annotated[Session, Depends(get_db_session)],
        symbol: StockCreate,
        ):
    find_symbol = db_session.exec(select(Stock.ticker_symbol).where(col(Stock.ticker_symbol) == symbol.ticker_symbol.upper())).one_or_none()
    if find_symbol:
        raise HTTPException(status_code=409, detail="Ticker symbol already exists.")

    try:
        stock_info = await stock.fetch_price(
                client,
                symbol.ticker_symbol.upper(),
                TWELVE_DATA_API_KEY
                )
        add_symbol = Stock(
                ticker_symbol=symbol.ticker_symbol.upper(),
                company_name=stock_info.get("name"),
                currency="USD"
                )
        db_session.add(add_symbol)
        db_session.commit()
        db_session.refresh(add_symbol)
        return add_symbol
    except (aiohttp.ClientResponseError, KeyError):
        raise HTTPException(status_code=404, detail="Stock could not be found. Please ensure you are using the correct ticker symbol.")


@router.get("/{symbol}", description="Return basic ticker symbol information.", response_model=StockPublic)
async def get_stock(
        db_session: Annotated[Session, Depends(get_db_session)],
        symbol: Annotated[str, Path(description="ETF ticker symbol.", min_length=1, max_length=5)],
        ):
    symbol = symbol.upper()
    try:
        # We use `one` here instead of `first` because we expect only one etf to return. Using `one` will return an MultipleResultsFound error if there is more than one result or NoResultFound.
        output_symbol = db_session.exec(select(Stock).where(col(Stock.ticker_symbol) == symbol)).one()
        return output_symbol
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Ticker symbol not found in the database.")


@router.delete("/{symbol}", description="Delete ticker symbol and all related information from the database.")
async def delete_stock(
        db_session: Annotated[Session, Depends(get_db_session)],
        symbol: Annotated[str, Path(description="ETF ticker symbol.", min_length=1, max_length=5)],
        ):
    symbol = symbol.upper()
    try:
        get_symbol = db_session.exec(select(Stock).where(col(Stock.ticker_symbol) == symbol)).one()
        db_session.delete(get_symbol)
        db_session.commit()
        return {"success": "Stock deleted successfully"}
    except NoResultFound:
        raise HTTPException(
                status_code=404,
                detail="Symbol not found.",
                )
    except MultipleResultsFound:
        raise HTTPException(
                status_code=500,
                detail="Expected exactly one resource, found multiple."
                )


@router.get("/{symbol}/price", description="Retrieve the latest closing price of a ticker symbol.", response_model=StockPricePublic)
async def get_price(
        client: Annotated[aiohttp.ClientSession, Depends(get_session)],
        db_session: Annotated[Session, Depends(get_db_session)],
        symbol: Annotated[str, Path(description="ETF ticker symbol.", min_length=1, max_length=5)],
        price_date: Annotated[date | None, Query(description="Retrieve price by a certain date. Must be YYYY-MM-DD formatted.")] = None
        ):
    symbol = symbol.upper()
    output: Dict[str, str|float|None]= {"ticker_symbol": symbol, "price_date": None, "close_price": None}

    try:
        symbol_id = db_session.exec(select(Stock.id).where(col(Stock.ticker_symbol) == symbol)).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Ticker symbol not found in the database.")

    if not price_date:
        latest_trading_day = get_latest_trading_day(date.today()).isoformat()
        data = db_session.exec(select(StockPrice).where(col(StockPrice.stock_id) == symbol_id, col(StockPrice.price_date) == latest_trading_day)).one_or_none()
        if not data:
            try:
                symbol_price = await stock.fetch_price(client, symbol, TWELVE_DATA_API_KEY)
                add_latest_price_data = StockPrice(
                        stock_id=cast(int, symbol_id),
                        price_date=symbol_price["date"],
                        close_price=cast(float, symbol_price["close_price"])
                        )
                db_session.add(add_latest_price_data)
                db_session.commit()
                output["price_date"], output["close_price"] = add_latest_price_data.price_date, add_latest_price_data.close_price
                return output
            except KeyError:
                raise HTTPException(status_code=404, detail=f"Price could not be obtained. Stock market could have been closed on date: {date.today().isoformat()}")

        output["price_date"], output["close_price"] = data.price_date, data.close_price
        return output

    if price_date:
        get_price_by_date = db_session.exec(select(StockPrice).where(col(StockPrice.price_date) == price_date, col(StockPrice.stock_id) == symbol_id)).one_or_none()
        if not get_price_by_date:
            try:
                symbol_date_price = await stock.fetch_date(client, symbol, str(price_date), TWELVE_DATA_API_KEY)
                add_price_data = StockPrice(
                        stock_id=cast(int, symbol_id),
                        price_date=str(price_date),
                        close_price=symbol_date_price["price"]
                        )
                db_session.add(add_price_data)
                db_session.commit()
                output["price_date"], output["close_price"] = add_price_data.price_date, add_price_data.close_price
                return output
            except aiohttp.ClientResponseError:
                raise HTTPException(status_code=404, detail="Could not find a price on that date. This could have been a weekend, holiday, or sometime in the future.")

        output["price_date"], output["close_price"] = get_price_by_date.price_date, get_price_by_date.close_price
        return output


@router.get("/{symbol}/news", description="Retrieve news articles on specific ticker symbol.")
async def get_news(client: Annotated[aiohttp.ClientSession, Depends(get_session)],
                   symbol: Annotated[str, Path(description="Get news for a stock by ticker symbol", min_length=1, max_length=5)]):
    symbol = symbol.upper()
    try:
        # Calls the stock service to fetch news from the external API
        return await stock.fetch_news(client=client, symbol=symbol, api_key=NEWS_DATA_API_KEY)
    except ValueError:
        # Handles the case where the API returns 0 results by returning a structured error message
        raise HTTPException(status_code=404, detail=f"Failed to find any news for {symbol}.")
    except aiohttp.ClientError as e:
        logger.error(f"Network error fetching news for {symbol}: {e}")
        raise HTTPException(status_code=502, detail="Failed to connect to the external news API.")


if __name__ == "__main__":
    # For testing purposes run `python -m backend.routers.stocks`.
    from ..services.lifespan import DatabaseManager

    db_session = DatabaseManager.get_db_session()

    with db_session as session:
        statement = select(StockPrice).where(StockPrice.stock_id == 1)
        result = session.exec(statement)
        spcx = result.all()
        print("This is what I want to see: ", [i.stock.ticker_symbol if i else None for i in spcx])
