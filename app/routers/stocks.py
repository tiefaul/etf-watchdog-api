from fastapi import APIRouter, Query, HTTPException, Path
from ..services.stock_service import Stock
from ..services.logger_service import setup_logging
from typing import Annotated
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("TWELVE_DATA_API_KEY")
logger = logging.getLogger(__name__)
setup_logging()

router = APIRouter(
        prefix="/api/stocks",
        tags=["stocks"],
        responses={404: {"description": "Page Not Found"}}
        )

stock = Stock()

@router.get("/", description="List all available stocks to track.")
async def get_all_stocks():
    stocks_dict = await stock.get_stocks()
    return stocks_dict

@router.get("/{symbol}")
async def get_stock(
        symbol: Annotated[str, Path(description="Get stock by ticker symbol.", min_length=1, max_length=5)],
        price: Annotated[bool | None, Query(description="Show current trading changes.")] = None,
        date: Annotated[str | None, Query(description="Retrieve price by date. Must be in 'year-month-day' format.")] = None
        ):

    stock_dict = await stock.get_stocks()
    if symbol.upper() in stock_dict["stocks"]:
        results = {"symbol": symbol.upper()}

        if price is True:
            stock_price = await stock.fetch_price(symbol=symbol.upper(), api_key=api_key)
            results.update({"stock_name": stock_price["name"],
                            "price_current": stock_price["price"],
                            "date": stock_price["date"],
                            "close_price": stock_price["close_price"]})

        if date:
            try:
                # Verify date format
                logger.debug("Verifying date format.")
                datetime.strptime(date, "%Y-%m-%d")
                stock_price_by_date = await stock.fetch_date(symbol=symbol.upper(), date=date, api_key=api_key)
                results.update({f"price_{date}": stock_price_by_date})
            except ValueError:
                results.update({"error": "Invalid date provided."})

        return results

    else:
        logger.error(f"{symbol} not found in the database.")
        raise HTTPException(status_code=404, detail=f"Symbol: '{symbol}' not found in the database.")
