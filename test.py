import requests
from dotenv import load_dotenv
import os

load_dotenv()

url = f"https://api.twelvedata.com/eod?symbol=AAPL&date=2025-10-23&apikey={os.getenv('API_KEY')}"

response = requests.get(url)

print(response.json())
