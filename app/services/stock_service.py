from dotenv import load_dotenv
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

        # Create a async request
        try:
            async with aiohttp.ClientSession(timeout=60) as request:
                async with request.get(url=f'{url}/eod?symbol=IYW&date={date}&apikey={api_key}') as response:
                    output = await response.json()
                    return output["close"]

        except KeyError:
            return f"This date does not appear in the stock data: {date}"

    async def get_current_price(self, url: str, api_key: str | None):
        async with aiohttp.ClientSession(timeout=60) as request:
            async with request.get(url=f'{url}/price?symbol=IYW&apikey={api_key}') as response:
                output = await response.json()
                return output["price"]

class SMH:
    async def get_price_by_date(self, url: str, date: str, api_key: str | None):
        try:
            datetime.strptime(date, "%Y-%m-%d") # Validate the date format
            # today_date = str(datetime.now().strftime("%Y-%m-%d")) # Outputs a string
        except ValueError as e:
            return f"Incorrect date format: {e}"

        try:
            async with aiohttp.ClientSession(timeout=60) as request:
                async with request.get(url=f'{url}/eod?symbol=SMH&date={date}&apikey={api_key}') as response:
                    output = await response.json()
                    return output["close"]

        except KeyError:
            return f"This date does not appear in the stock data: {date}"

    async def get_current_price(self, url: str, api_key: str | None):
        async with aiohttp.ClientSession(timeout=60) as request:
            async with request.get(url=f'{url}/price?symbol=SMH&apikey={api_key}') as response:
                output = await response.json()
                return output["price"]

class SPY:
    async def get_price_by_date(self, url: str, date: str, api_key: str | None):
        try:
            datetime.strptime(date, "%Y-%m-%d") # Validate the date format
            # today_date = str(datetime.now().strftime("%Y-%m-%d")) # Outputs a string
        except ValueError as e:
            return f"Incorrect date format: {e}"

        try:
            async with aiohttp.ClientSession(timeout=60) as request:
                async with request.get(url=f'{url}/eod?symbol=SPY&date={date}&apikey={api_key}') as response:
                    output = await response.json()
                    return output["close"]

        except KeyError:
            return f"This date does not appear in the stock data: {date}"

    async def get_current_price(self, url: str, api_key: str | None):
        async with aiohttp.ClientSession(timeout=60) as request:
            async with request.get(url=f'{url}/price?symbol=SPY&apikey={api_key}') as response:
                output = await response.json()
                return output["price"]

class DRIV:
    async def get_price_by_date(self, url: str, date: str, api_key: str | None):
        try:
            datetime.strptime(date, "%Y-%m-%d") # Validate the date format
            # today_date = str(datetime.now().strftime("%Y-%m-%d")) # Outputs a string
        except ValueError as e:
            return f"Incorrect date format: {e}"

        try:
            async with aiohttp.ClientSession(timeout=60) as request:
                async with request.get(url=f'{url}/eod?symbol=DRIV&date={date}&apikey={api_key}') as response:
                    output = await response.json()
                    return output["close"]

        except KeyError:
            return f"This date does not appear in the stock data: {date}"

    async def get_current_price(self, url: str, api_key: str | None):
        async with aiohttp.ClientSession(timeout=60) as request:
            async with request.get(url=f'{url}/price?symbol=DRIV&apikey={api_key}') as response:
                output = await response.json()
                return output["price"]

class IGV:
    async def get_price_by_date(self, url: str, date: str, api_key: str | None):
        try:
            datetime.strptime(date, "%Y-%m-%d") # Validate the date format
            # today_date = str(datetime.now().strftime("%Y-%m-%d")) # Outputs a string
        except ValueError as e:
            return f"Incorrect date format: {e}"

        try:
            async with aiohttp.ClientSession(timeout=60) as request:
                async with request.get(url=f'{url}/eod?symbol=IGV&date={date}&apikey={api_key}') as response:
                    output = await response.json()
                    return output["close"]

        except KeyError:
            return f"This date does not appear in the stock data: {date}"

    async def get_current_price(self, url: str, api_key: str | None):
        async with aiohttp.ClientSession(timeout=60) as request:
            async with request.get(url=f'{url}/price?symbol=IGV&apikey={api_key}') as response:
                output = await response.json()
                return output["price"]

class CIBR:
    async def get_price_by_date(self, url: str, date: str, api_key: str | None):
        try:
            datetime.strptime(date, "%Y-%m-%d") # Validate the date format
            # today_date = str(datetime.now().strftime("%Y-%m-%d")) # Outputs a string
        except ValueError as e:
            return f"Incorrect date format: {e}"

        try:
            async with aiohttp.ClientSession(timeout=60) as request:
                async with request.get(url=f'{url}/eod?symbol=CIBR&date={date}&apikey={api_key}') as response:
                    output = await response.json()
                    return output["close"]

        except KeyError:
            return f"This date does not appear in the stock data: {date}"

    async def get_current_price(self, url: str, api_key: str | None):
        async with aiohttp.ClientSession(timeout=60) as request:
            async with request.get(url=f'{url}/price?symbol=CIBR&apikey={api_key}') as response:
                output = await response.json()
                return output["price"]

class SHY:
    async def get_price_by_date(self, url: str, date: str, api_key: str | None):
        try:
            datetime.strptime(date, "%Y-%m-%d") # Validate the date format
            # today_date = str(datetime.now().strftime("%Y-%m-%d")) # Outputs a string
        except ValueError as e:
            return f"Incorrect date format: {e}"

        try:
            async with aiohttp.ClientSession(timeout=60) as request:
                async with request.get(url=f'{url}/eod?symbol=SHY&date={date}&apikey={api_key}') as response:
                    output = await response.json()
                    return output["close"]

        except KeyError:
            return f"This date does not appear in the stock data: {date}"

    async def get_current_price(self, url: str, api_key: str | None):
        async with aiohttp.ClientSession(timeout=60) as request:
            async with request.get(url=f'{url}/price?symbol=SHY&apikey={api_key}') as response:
                output = await response.json()
                return output["price"]

async def get_all_stocks():
    return {"stocks": ["SHY", "CIBR", "IGV", "DRIV", "SPY", "SMH", "IYW"]}

if __name__ == "__main__":
    shy = SHY()
    print(asyncio.run(shy.get_current_price(url=url, api_key=api_key)))
