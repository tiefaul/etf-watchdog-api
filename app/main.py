from fastapi import FastAPI
from .routers import stocks
from contextlib import asynccontextmanager
from fastapi.logger import logger as fastAPI_logger  # convenient name
from .services.aiohttp_client_service import HttpClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load aiohttp ClientSession
    fastAPI_logger.info("Starting aiohttp client for Stock router")
    http_client = HttpClient()
    http_client.start_http_client()
    yield {"http_client": http_client.get_session()}
    # Shutdown aiohttp ClientSession
    fastAPI_logger.info("Closing aiohttp client for Stock router")
    await http_client.stop_http_client()


app = FastAPI(lifespan=lifespan)
app.include_router(stocks.router)


@app.get("/api")
async def main():
    pass
