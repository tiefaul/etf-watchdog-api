from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()

url = "https://www.alphavantage.co"
api_key = os.getenv("API_KEY")

response = requests.get(f'{url}/query?function=TIME_SERIES_WEEKLY&symbol=IYW&apikey={api_key}')

display_data = json.dumps(response.json(), indent=2)

# print(response.json()[0])

print(display_data)
