from fastapi import FastAPI
from .routers import stocks
from contextlib import asynccontextmanager
from fastapi.logger import logger as fastAPI_logger
from .services.lifespan import HttpClient, DatabaseManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database
    fastAPI_logger.info("Initializing the database.")
    DatabaseManager.init_db()

    # Load aiohttp ClientSession
    fastAPI_logger.info("Starting aiohttp client.")
    http_client = HttpClient()
    http_client.start_http_client()

    yield {"http_client": http_client.get_session(), "db_session": DatabaseManager.get_db_session()}

    # Shutdown aiohttp ClientSession
    fastAPI_logger.info("Closing aiohttp client for Stock router.")
    await http_client.stop_http_client()


app = FastAPI(lifespan=lifespan)
app.include_router(stocks.router)


@app.get("/api", description="This does nothing at the moment")
async def main():
    pass
