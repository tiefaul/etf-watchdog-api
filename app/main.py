from fastapi import FastAPI
from .routers import stocks
from fastapi.responses import HTMLResponse

app = FastAPI()

app.include_router(router=stocks.router)

@app.get("/api", response_class=HTMLResponse)
async def main():
    return "<h1>Welcome to my stocks tracker website!<h1>"
