from textwrap import indent
from dotenv import load_dotenv
import requests
import os
from datetime import datetime
import json

load_dotenv()

url = "https://www.alphavantage.co"
api_key = os.getenv("API_KEY")

response = requests.get(f'{url}/query?function=TIME_SERIES_INTRADAY&symbol=IYW&interval=5min&apikey={api_key}')

display_data = json.dumps(response.json(), indent=2)

print(display_data)
