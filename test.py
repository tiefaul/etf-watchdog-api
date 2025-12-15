import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

# parameters = {
#     "qInMeta": "IYW",
#     "apikey": os.getenv("NEWS_DATA_API_KEY"),
#     "language": "en"
#         }
#
# url = "https://newsdata.io/api/1/?apikey=pub_b5bccfae5ae44288aa661ebb96994b5b&q=IYW"
# response = requests.get(url)
# data = response.json()
# print(json.dumps(data, indent=4))

parameters = {
        "symbol": "IYW",
        "apikey": os.getenv("TWELVE_DATA_API_KEY"),
        "datetime": "2025-12-11"
        }

url = "https://api.twelvedata.com/quote"
response = requests.get(url, params=parameters).json()
print(json.dumps(response, indent=4))
