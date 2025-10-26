from fastapi import APIRouter, Query, HTTPException
from ..services import stock_service
from typing import Annotated

router = APIRouter(
        prefix="/api/stocks",
        tags=["stocks"],
        responses={
            404: {"description": "Page Not Found"}
            }
        )

@router.get("/")
async def get_all_stocks(stock: Annotated[str | None, Query(description="Retrieve stock by the stock's ticker symbol", min_length=1, max_length=5)] = None):
    stocks_dict = await stock_service.get_all_stocks()
    # If query is given
    if stock is not None:
        if stock in stocks_dict["stocks"]:
            return stock
        else:
            raise HTTPException(status_code=404, detail=f"{stock} symbol not found.")
    # Else return all stocks
    return stocks_dict
