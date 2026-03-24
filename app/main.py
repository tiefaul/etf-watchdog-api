from fastapi import FastAPI
from .routers import stocks
from fastapi.logger import logger as fastAPI_logger  # convenient name
from contextlib import asynccontextmanager
from .services.aiohttp_client_service import HttpClient

http_client = HttpClient()

app = FastAPI()

app.include_router(router=stocks.router)

@app.get("/api")
async def main():
    pass
