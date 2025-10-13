from dotenv import load_dotenv
import requests
import os
from datetime import datetime
import asyncio
import aiohttp

load_dotenv()

url = "https://api.twelvedata.com"
api_key = os.getenv("API_KEY")

class IYW:
    async def get_price_by_date(self, url: str, date: str, api_key: str | None):
        try:
            datetime.strptime(date, "%Y-%m-%d") # Validate the date format
            # today_date = str(datetime.now().strftime("%Y-%m-%d")) # Outputs a string
        except ValueError as e:
            return f"Incorrect date format: {e}"

        try:
            async with aiohttp.ClientSession() as request:
                async with request.get(url=f'{url}/eod?symbol=IYW&date={date}&apikey={api_key}') as response:
                    output = await response.json()
                    return output["close"]

        except KeyError:
            return f"This date does not appear in the stock data: {date}"

    async def get_current_price(self, url: str, api_key: str | None):
        async with aiohttp.ClientSession() as request:
            async with request.get(url=f'{url}/price?symbol=IYW&apikey={api_key}') as response:
                output = await response.json()
                return output["price"]

if __name__ == "__main__":
    iyw = IYW()
    print(asyncio.run(iyw.get_current_price(url=url, api_key=api_key)))
