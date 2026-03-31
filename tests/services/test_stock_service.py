import aiohttp
from app.services.stock_service import Stock
import asyncio

class MockGetStocksResponse:
    @staticmethod
    def json():
        return {"price": "fakeprice", "close_price": "fakecloseprice", "date": "fakedate", "name": "fakename"}

def test_get_stocks(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockGetStocksResponse()

    monkeypatch.setattr(aiohttp.ClientSession, "get", mock_get)
    results = asyncio.run(Stock.fetch_price(symbol="fakesymbol", api_key="fakeapikey"))

    output = {"price": "fakeprice", "close_price": "fakecloseprice", "date": "fakedate", "name": "fakename"}
    assert results == output
