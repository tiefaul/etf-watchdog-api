from fastapi import FastAPI
from .routers import stocks
from fastapi.logger import logger as fastAPI_logger  # convenient name
from .services.stock_service import Stock
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load aiohttp ClientSession
    fastAPI_logger.info("Starting Stock aiohttp client")
    Stock.get_stock_client()
    yield
    # Shutdown aiohttp ClientSession
    fastAPI_logger.info("Shutting down Stock aiohttp client")
    await Stock.close_stock_client()

app = FastAPI(lifespan=lifespan)

app.include_router(router=stocks.router)

@app.get("/api")
async def main():
    pass
