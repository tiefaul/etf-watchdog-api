from app.services.stock_service import Stock
import pytest

stock = Stock()
twelve_url = "https://api.twelvedata.com"

def test_get_stocks():
    func = stock.get_stocks()
    assert isinstance(func, dict)
    assert "stocks" in func
    assert isinstance(func["stocks"], set)


@pytest.mark.asyncio
async def test_fetch_price(mock_response, async_client):
    func = stock.fetch_price
    response = {"open": "123", "close": "12343", "datetime": "2026-04-26", "name": "fake"}
    mock_response.get(f"{twelve_url}/quote?symbol=FAKE&apikey=faketoken", status=200, payload=response)
    data = await func(session=async_client, symbol="FAKE", api_key="faketoken")
    assert isinstance(data, dict)
    assert isinstance(data["price"], str)
    assert isinstance(data["close_price"], str)
    assert isinstance(data["date"], str)
    assert isinstance(data["name"], str)
    # make sure func raises a KeyError
    with pytest.raises(KeyError):
        assert data["wrong_key"]


@pytest.mark.asyncio
async def test_fetch_date(mock_response, async_client):
    func = stock.fetch_date 
    response = {"close": "123.34"}
    mock_response.get(f"{twelve_url}/eod?symbol=fake&date=2026-03-18&apikey=faketoken", payload=response)
    data = await func(session=async_client, symbol="fake", date="2026-03-18", api_key="faketoken")
    assert isinstance(data, dict)
    assert isinstance(data["date"], str)
    with pytest.raises(KeyError):
        assert data["wrong_key"]

