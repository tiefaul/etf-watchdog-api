from fastapi import FastAPI
from .routers import stocks
from fastapi.logger import logger as fastAPI_logger  # convenient name
from .services.stock_service import Stock

async def on_start_up() -> None:
    fastAPI_logger.info("Starting Stock aiohttp client")
    Stock.get_stock_client()

async def on_shutdown() -> None:
    fastAPI_logger.info("Shutting down Stock aiohttp client")
    await Stock.close_stock_client()

app = FastAPI(on_startup=[on_start_up], on_shutdown=[on_shutdown])

app.include_router(router=stocks.router)

@app.get("/api")
async def main():
    pass
