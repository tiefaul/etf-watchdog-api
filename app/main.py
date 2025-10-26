from fastapi import FastAPI
from .routers import stocks

app = FastAPI()

app.include_router(router=stocks.router)

@app.get("/api")
async def main():
    pass
