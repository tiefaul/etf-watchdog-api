from dotenv import load_dotenv
import os
from datetime import datetime
import asyncio
import aiohttp
from fastapi import HTTPException

load_dotenv()

class Stock:
    # Retrieve all monitored stocks
    async def get_stocks(self):
        return {"stocks": ["SHY", "CIBR", "IGV", "DRIV", "SPY", "SMH", "IYW"]}

    # Get price for stock by date
    async def get_price_by_date(self, url: str, date: str, symbol: str, api_key: str | None):
        stock = await self.get_stocks()
        if symbol not in stock["stocks"]:
            raise HTTPException(status_code=404, detail=f"Symbol: {symbol} not in the database.")
        try:
            datetime.strptime(date, "%Y-%m-%d") # Validate the date format
            # today_date = str(datetime.now().strftime("%Y-%m-%d")) # Outputs a string
        except ValueError as e:
            raise HTTPException(status_code=404, detail= f"Incorrect date format: {e}")

        # Create a async request
        try:
            async with aiohttp.ClientSession() as request:
                async with request.get(url=f'{url}/eod?symbol={symbol}&date={date}&apikey={api_key}') as response:
                    output = await response.json()
                    return output["close"]

        except KeyError as e:
            raise HTTPException(status_code=404, detail= f"{date} does not appear in the stock data: {e}")

    # Get current price of stock
    async def get_current_price(self, url: str, symbol: str, api_key: str | None):
        stock = await self.get_stocks() # Get all stocks in the database and raise an error if it doesn't exist
        if symbol not in stock["stocks"]:
            raise HTTPException(status_code=404, detail=f"Symbol: {symbol} not in the database.")

        # Create async request
        async with aiohttp.ClientSession() as request:
            async with request.get(url=f'{url}/price?symbol={symbol}&apikey={api_key}') as response:
                output = await response.json()
                return output["price"]

if __name__ == "__main__":
    url = "https://api.twelvedata.com"
    api_key = os.getenv("API_KEY")
    stock = Stock()
    print(asyncio.run(stock.get_current_price(url=url, symbol="IYW", api_key=api_key)))
