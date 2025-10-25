from fastapi import APIRouter
from ..services import stock_service

router = APIRouter(
        prefix="/api/stocks",
        tags=["stocks"],
        responses={
            404: {"description": "Page Not Found"}
            }
        )

@router.get("/")
async def get_all_stocks():
    return stock_service.get_all_stocks()

@router.get("/{stock_int}")
async def get_stock_list(stock_int: int):
    return stock_service.get_all_stocks()[stock_int]


@router.get("/IYW")
async def get_iyw():
    pass
