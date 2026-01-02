from app.services.stock_service import Stock
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

api_key = os.getenv("TWELVE_DATA_API_KEY")

stock = Stock()

test = asyncio.run(stock.fetch_price(symbol="IYW", api_key=api_key))

print(test)
