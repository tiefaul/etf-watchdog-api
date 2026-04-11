from app.services.stock_service import Stock
import pytest

stock = Stock()

def test_get_stocks():
    func = stock.get_stocks()
    assert isinstance(func, dict)
    assert "stocks" in func
    assert isinstance(func["stocks"], set)


@pytest.mark.asyncio
async def test_fetch_price(mock_response, async_client):
    url = "https://api.twelvedata.com"
    response = {"price": "1234", "close_price": "12343", "date": "datetime", "name": "fake"}
    mock_response.get(f"{url}/quote?symbol=FAKE&apikey=faketoken", status=200, payload=response)
    data = await stock.fetch_price(session=async_client, symbol="FAKE", api_key="faketoken")
    assert isinstance(data, dict)
