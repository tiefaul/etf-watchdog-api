from fastapi import APIRouter

router = APIRouter(
        prefix="/stocks",
        tags=["Stocks"],
        responses={
            404: {"description": "Page Not Found"}
            }
        )

@router.get("/")
async def get_all_stocks():
    pass

@router.get("/IYW")
async def get_iyw():
    pass
