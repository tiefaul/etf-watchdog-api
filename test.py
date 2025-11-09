import requests
from dotenv import load_dotenv
import os

load_dotenv()

url = f"https://api.twelvedata.com/etfs/world/summary?symbol=IYW&apikey={os.getenv('TWELVE_DATA_API_KEY')}"

response = requests.get(url)

print(response.json())
