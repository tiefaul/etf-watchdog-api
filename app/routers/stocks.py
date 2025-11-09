from fastapi import APIRouter, Query, HTTPException, Path
from ..services.stock_service import Stock
from ..services.logger_service import setup_logging
from typing import Annotated
import os
import logging
from datetime import datetime

url = "https://api.twelvedata.com"
api_key = os.getenv("TWELVE_DATA_API_KEY")
logger = logging.getLogger(__name__)
setup_logging()

router = APIRouter(
        prefix="/api/stocks",
        tags=["stocks"],
        responses={
            404: {"description": "Page Not Found"}
            }
        )

@router.get("/", description="List all available stocks to track.")
async def get_all_stocks():
    stock = Stock()
    stocks_dict = await stock.get_stocks()
    return stocks_dict

@router.get("/{symbol}")
async def get_stock(
        symbol: Annotated[str, Path(description="Get stock by ticker symbol.", min_length=1, max_length=5)],
        price: Annotated[bool | None, Query(description="Show the current trading price.")] = None,
        date: Annotated[str | None, Query(description="Retrieve price by date. Must be in 'year-month-day' format.")] = None
        ):

    stock = Stock()
    stock_dict = await stock.get_stocks()
    if symbol.upper() in stock_dict["stocks"]:
        results = {"symbol": symbol.upper()}

        if price is True:
            stock_price = await stock.get_current_price(url=url, symbol=symbol.upper(), api_key=api_key) #type: ignore
            results.update({"price_current": stock_price})

        if date:
            try:
                datetime.strptime(date, "%Y-%m-%d")
                stock_price_by_date = await stock.get_price_by_date(url=url, symbol=symbol.upper(), date=date, api_key=api_key) #type: ignore
                results.update({f"price_{date}": stock_price_by_date})

            except ValueError as e:
                logger.error(f"Incorrect date format: {e}", exc_info=True)
                raise HTTPException(status_code=404, detail=f"Incorrect date format ({date}): {e}")

        return results

    else:
        logger.error(f"{symbol} not found in the database.")
        raise HTTPException(status_code=404, detail=f"{symbol} not found in the database.")
