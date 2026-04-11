from fastapi import FastAPI
from .routers import stocks
from .services.aiohttp_client_service import HttpClient


app = FastAPI()
app.include_router(router=stocks.router)


@app.get("/api")
async def main():
    pass
