from fastapi import APIRouter, Query, HTTPException
from ..services.stock_service import Stock
from typing import Annotated

router = APIRouter(
        prefix="/api/stocks",
        tags=["stocks"],
        responses={
            404: {"description": "Page Not Found"}
            }
        )

@router.get("/")
async def get_all_stocks(symbol: Annotated[str | None, Query(description="Retrieve stock by the stock's ticker symbol", min_length=1, max_length=5)] = None):
    stock = Stock()
    stocks_dict = await stock.get_stocks()
    # If query is given
    if symbol is not None:
        if symbol in stocks_dict["stocks"]:
            return symbol
        else:
            raise HTTPException(status_code=404, detail=f"{symbol} symbol not found.")
    # Else return all stocks
    return stocks_dict
