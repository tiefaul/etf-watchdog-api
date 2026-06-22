import pytest


TWELVE_URL = "https://api.twelvedata.com"
NEW_DATA_URL = "https://newsdata.io/api/1"


@pytest.mark.asyncio
async def test_fetch_price_success(mock_response, async_client, stock_service):
    func = stock_service.fetch_price
    response = {"open": "123", "close": "12343.0", "datetime": "2026-04-26", "name": "fake"}
    mock_response.get(f"{TWELVE_URL}/quote?symbol=FAKE&apikey=faketoken", status=200, payload=response)
    data = await func(client=async_client, symbol="FAKE", api_key="faketoken")
    assert isinstance(data, dict)
    assert data["price"] == "123" # NOTE something needs to be done with this.
    assert data["close_price"] == 12343.0
    assert data["date"] == "2026-04-26"
    assert data["name"] == "fake"


@pytest.mark.asyncio
async def test_fetch_price_raises_key_error(mock_response, async_client, stock_service):
    func = stock_service.fetch_price
    with pytest.raises(KeyError, match="Error when fetching the price data."):
        mock_response.get(f"{TWELVE_URL}/quote?symbol=FAKE&apikey=faketoken", status=200, payload={})
        await func(client=async_client, symbol="FAKE", api_key="faketoken")


@pytest.mark.asyncio
async def test_fetch_date_success(mock_response, async_client, stock_service):
    func = stock_service.fetch_date
    response = {"close": "123.34"}
    mock_response.get(f"{TWELVE_URL}/eod?symbol=fake&date=2026-03-18&apikey=faketoken", status=200, payload=response)
    data = await func(client=async_client, symbol="fake", date="2026-03-18", api_key="faketoken")
    assert isinstance(data, dict)
    assert data["price"] == 123.34


@pytest.mark.asyncio
async def test_fetch_date_raises_key_error(mock_response, async_client, stock_service):
    func = stock_service.fetch_date
    with pytest.raises(KeyError, match="Error when fetching the date."):
        mock_response.get(f"{TWELVE_URL}/eod?symbol=fake&date=2026-03-18&apikey=faketoken", status=200, payload={})
        await func(client=async_client, symbol="fake", date="2026-03-18", api_key="faketoken")


@pytest.mark.asyncio
async def test_fetch_news_success(mock_response, async_client, stock_service):
    func = stock_service.fetch_news
    response = {"totalResults": 1,
                "results": [
                    {
                        "link": "https://www.fakenews.com",
                        "description": "My fake description",
                        }
                    ]
                }

    mock_response.get(f"{NEW_DATA_URL}/market?qInTitle=FAKE&apikey=fakeapikey", status=200, payload=response)
    data = await func(client=async_client, symbol="FAKE", api_key="fakeapikey")
    assert isinstance(data, dict)
    assert isinstance(data["totalResults"], int)
    assert isinstance(data["articles"], list)


@pytest.mark.asyncio
async def test_fetch_news_raises_value_error(mock_response, async_client, stock_service):
    func = stock_service.fetch_news
    response = {"totalResults": 0,
                "results": [
                {
                    "link": "https://www.fakenews.com",
                    "description": "My fake description",
                    }
                ]
            }
    mock_response.get(f"{NEW_DATA_URL}/market?qInTitle=FAKE&apikey=fakeapikey", status=200, payload=response)
    with pytest.raises(ValueError, match="News API returned 0 results."):
        await func(client=async_client, symbol="FAKE", api_key="fakeapikey")
