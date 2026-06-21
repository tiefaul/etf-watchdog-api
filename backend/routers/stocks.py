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
from typing import Annotated, List, cast
from datetime import date
from dotenv import load_dotenv
from sqlmodel import Session, select, col
from sqlalchemy.exc import IntegrityError, NoResultFound
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
        tags=["stocks"],
        responses={404: {"description": "Page Not Found"}},
        )


def validate_add_commit_refresh(model, session: Session, **kwargs):
    data = model(
            **kwargs
            )
    output = model.model_validate(data)
    session.add(output)
    session.commit()
    session.refresh(output)
    return output


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
    # NOTE: Need to check if the symbol is already in the database and raise an error. This is calling the external API on every post request.
    try:
        stock_info = await stock.fetch_price(
                client,
                symbol.ticker_symbol.upper(),
                TWELVE_DATA_API_KEY
                )
        return validate_add_commit_refresh(
                Stock,
                db_session,
                ticker_symbol=symbol.ticker_symbol.upper(),
                company_name=stock_info.get("name"),
                currency="USD"
                )

    except aiohttp.ClientResponseError:
        raise HTTPException(status_code=404, detail="Stock could not be found. Please ensure you are using the correct ticker symbol.")
    except IntegrityError:
        db_session.rollback()
        raise HTTPException(status_code=409, detail="Ticker symbol already exists.")


@router.get("/{symbol}", description="Return basic ticker symbol information.", response_model=StockPublic)
async def get_stock(
        db_session: Annotated[Session, Depends(get_db_session)],
        symbol: Annotated[str, Path(description="ETF ticker symbol.", min_length=1, max_length=5)],
        ):
    symbol = symbol.upper()
    try:
        # We use `one` here instead of `first` because we expect only one etf to return. Using `one` will return an MultipleResultsFound error if there is more than one result.
        data = db_session.exec(select(Stock).where(col(Stock.ticker_symbol) == symbol)).one()
        return data
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Ticker symbol not found in the database.")


@router.get("/{symbol}/price", description="Retrieve the latest closing price of a ticker symbol.", response_model=StockPricePublic)
async def get_price(
        client: Annotated[aiohttp.ClientSession, Depends(get_session)],
        db_session: Annotated[Session, Depends(get_db_session)],
        symbol: Annotated[str, Path(description="ETF ticker symbol.", min_length=1, max_length=5)],
        date: Annotated[date | None, Query(description="Retrieve price by a certain date. Must be YYYY-MM-DD formatted.")] = None
        ):
    symbol = symbol.upper()
    output = {"ticker_symbol": symbol, "price_date": None, "close_price": None}
    try:
        etf_id = db_session.exec(select(Stock.id).where(col(Stock.ticker_symbol) == symbol)).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Ticker symbol not found in the database.")
    # NOTE: This query will return the first result and not the latest price for the stock.
    data = db_session.exec(select(StockPrice).where(col(StockPrice.stock_id) == etf_id)).first()
    if not data:
        try:
            symbol_price = await stock.fetch_price(client, symbol, TWELVE_DATA_API_KEY)
            current_price_data = validate_add_commit_refresh(
                    StockPrice,
                    db_session,
                    stock_id=etf_id,
                    price_date=symbol_price["date"],
                    close_price=cast(float, symbol_price["close_price"])
                    )
            output["price_date"], output["close_price"] = current_price_data.price_date, current_price_data.close_price
            return output
        except KeyError as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error has occured: {e}")

    if date:
        get_price_by_date = db_session.exec(select(StockPrice).where(col(StockPrice.price_date) == date, col(StockPrice.stock_id) == etf_id)).first()
        if not get_price_by_date:
            try:
                symbol_date_price = await stock.fetch_date(client, symbol, str(date), TWELVE_DATA_API_KEY)
            except aiohttp.ClientResponseError:
                raise HTTPException(status_code=404, detail="Could not find a price on that date. This could have been a holiday or sometime in the future.")
            price_data = validate_add_commit_refresh(
                    StockPrice,
                    db_session,
                    stock_id=etf_id,
                    price_date=str(date),
                    close_price=symbol_date_price["date"]
                    )
            output["price_date"], output["close_price"] = price_data.price_date, price_data.close_price
            return output

        output["price_date"], output["close_price"] = get_price_by_date.price_date, get_price_by_date.close_price
        return output

    output["price_date"], output["close_price"] = data.price_date, data.close_price
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
