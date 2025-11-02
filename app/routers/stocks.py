from fastapi import APIRouter, Query, HTTPException, Path
from ..services.stock_service import Stock
from typing import Annotated
import datetime
import os

url = "https://api.twelvedata.com"
api_key = os.getenv("API_KEY")

router = APIRouter(
        prefix="/api/stocks",
        tags=["stocks"],
        responses={
            404: {"description": "Page Not Found"}
            }
        )

@router.get("/")
async def get_all_stocks():
    stock = Stock()
    stocks_dict = await stock.get_stocks()
    return stocks_dict

@router.get("/{symbol}")
async def get_stock(
        symbol: Annotated[str | None, Path(description="Get stock by ticker symbol.", min_length=1, max_length=5)],
        price: Annotated[bool | None, Query(description="Show the current trading price.")] = None,
        date: Annotated[str | None, Query(description="Retrieve price by date. Must be in 'year-month-day' format.")] = None
        ):

    stock = Stock()
    stock_dict = await stock.get_stocks()
    if symbol in stock_dict["stocks"]:
        results = {"symbol": symbol}
        if price is True:
            stock_price = await stock.get_current_price(url=url, symbol=symbol, api_key=api_key) #type: ignore
            results.update({"price_current": stock_price})
        if date:
            stock_price_by_date = await stock.get_price_by_date(url=url, symbol=symbol, date=date, api_key=api_key) #type: ignore
            results.update({f"price_{date}": stock_price_by_date})

        return results

    else:
        raise HTTPException(status_code=404, detail=f"Symbol: {symbol} not found in the database.")
