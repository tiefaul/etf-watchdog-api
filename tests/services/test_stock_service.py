import pytest


twelve_url = "https://api.twelvedata.com"
new_data_url = "https://newsdata.io/api/1"


def test_get_stocks_success(stock_service):
    data = stock_service.get_stocks()
    assert isinstance(data, dict)
    assert "stocks" in data
    assert isinstance(data["stocks"], set)


@pytest.mark.asyncio
async def test_fetch_price_success(mock_response, async_client, stock_service):
    func = stock_service.fetch_price
    response = {"open": "123", "close": "12343.0", "datetime": "2026-04-26", "name": "fake"}
    mock_response.get(f"{twelve_url}/quote?symbol=FAKE&apikey=faketoken", status=200, payload=response)
    data = await func(client=async_client, symbol="FAKE", api_key="faketoken")
    assert isinstance(data, dict)
    assert data["price"] == "123" # NOTE something needs to be done with this.
    assert data["close_price"] == 12343.0
    assert data["date"] == "2026-04-26"
    assert data["name"] == "fake"


@pytest.mark.asyncio
async def test_fetch_price_raises_key_error(mock_response, async_client, stock_service):
    func = stock_service.fetch_price
    with pytest.raises(KeyError):
        mock_response.get(f"{twelve_url}/quote?symbol=FAKE&apikey=faketoken", status=200, payload={})
        data = await func(client=async_client, symbol="FAKE", api_key="faketoken")
        assert "Error when fetching the price data." in data


@pytest.mark.asyncio
async def test_fetch_date_success(mock_response, async_client, stock_service):
    func = stock_service.fetch_date
    response = {"close": "123.34"}
    mock_response.get(f"{twelve_url}/eod?symbol=fake&date=2026-03-18&apikey=faketoken", status=200, payload=response)
    data = await func(client=async_client, symbol="fake", date="2026-03-18", api_key="faketoken")
    assert isinstance(data, dict)
    assert data["date"] == "123.34"


@pytest.mark.asyncio
async def test_fetch_date_raises_key_error(mock_response, async_client, stock_service):
    func = stock_service.fetch_date
    with pytest.raises(KeyError):
        mock_response.get(f"{twelve_url}/eod?symbol=fake&date=2026-03-18&apikey=faketoken", status=200, payload={})
        data = await func(client=async_client, symbol="fake", date="2026-03-18", api_key="faketoken")
        assert "Error when fetching the date" in data


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

    mock_response.get(f"{new_data_url}/market?qInTitle=FAKE&apikey=fakeapikey", status=200, payload=response)
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
    mock_response.get(f"{new_data_url}/market?qInTitle=FAKE&apikey=fakeapikey", status=200, payload=response)
    with pytest.raises(ValueError):
        data = await func(client=async_client, symbol="FAKE", api_key="fakeapikey")
        assert "News API returned 0 results." in data
