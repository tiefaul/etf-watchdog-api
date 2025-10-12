from dotenv import load_dotenv
import requests
import os
from datetime import datetime

load_dotenv()

url = "https://www.alphavantage.co"
api_key = os.getenv("API_KEY")

class Stocks:
    def __init__(self, base_url: str, api_key: str | None = None):
        self.api_key = os.getenv("API_KEY")
        self.base_url = "https://www.alphavantage.co"

    def IYW(self):
        today_date = str(datetime.now().strftime("%Y-%m-%d")) # TODO: Make this a string somehow
        response = requests.get(url=f'{self.base_url}/query?function=TIME_SERIES_DAILY&symbol=IYW&outputsize=compact&apikey={self.api_key}')
        output = response.json()
        # return json.dumps(output, indent=2)
        return output["Time Series (Daily)"]["2025-10-10"]["1. open"] # todo: make a variable for the daily open and then daily close

stock = Stocks(base_url=url, api_key=api_key)
print(stock.IYW())

# The best way to structure an API call in Python is to encapsulate the logic in a class or function that accepts the URL, API key, query parameters, and payload as arguments. Use the requests library for HTTP calls. Here’s a recommended structure:
#
# 1. **Configuration**: Store API URL and key in environment variables or a config file.
# 2. **Function or Class**: Create a reusable function or class method for making requests.
# 3. **Parameters**: Accept URL, headers (with API key), query params, and payload as arguments.
# 4. **Error Handling**: Handle exceptions and check response status codes.
#
# Example using a class:
#
# ```python
# import requests
#
# class APIClient:
#     def __init__(self, base_url, api_key):
#         self.base_url = base_url
#         self.headers = {"Authorization": f"Bearer {api_key}"}
#
#     def make_request(self, endpoint, method="GET", params=None, data=None, json=None):
#         url = f"{self.base_url}/{endpoint}"
#         response = requests.request(
#             method,
#             url,
#             headers=self.headers,
#             params=params,
#             data=data,
#             json=json,
#             timeout=10
#         )
#         response.raise_for_status()
#         return response.json()
# ```
#
# This structure is flexible, reusable, and easy to test.
