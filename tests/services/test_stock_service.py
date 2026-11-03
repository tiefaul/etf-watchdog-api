import pytest
from types import SimpleNamespace

import aiohttp

from backend.services.stock_service import FetchDatePriceModel, FetchQuoteModel


TWELVE_URL = "https://api.twelvedata.com"
NEWS_DATA_URL = "https://newsdata.io/api/1"


class MockHTTPResponse:
    def __init__(self, payload: dict, status: int = 200, url: str = ""):
        self._payload = payload
        self.status = status
        self._url = url

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    def raise_for_status(self):
        if self.status >= 400:
            raise aiohttp.ClientResponseError(
                request_info=SimpleNamespace(real_url=self._url),
                history=(),
                status=self.status,
                message="mocked error",
            )

    async def json(self):
        return self._payload


def _patch_get(monkeypatch, async_client, *, expected_url: str, expected_params: dict, payload: dict, status: int = 200):
    def fake_get(url, *, params=None, **kwargs):
        assert url == expected_url
        assert params == expected_params
        return MockHTTPResponse(payload=payload, status=status, url=url)

    monkeypatch.setattr(async_client, "get", fake_get)


@pytest.mark.asyncio
async def test_fetch_quote_data_success(monkeypatch, async_client, stock_service):
    func = stock_service.fetch_quote_data
    response = {"open": "123", "close": "12343.0", "datetime": "2026-04-26", "name": "fake"}
    _patch_get(
        monkeypatch,
        async_client,
        expected_url=f"{TWELVE_URL}/quote",
        expected_params={"symbol": "FAKE", "apikey": "faketoken"},
        payload=response,
    )
    data = await func(client=async_client, symbol="FAKE", api_key="faketoken")
    assert isinstance(data, FetchQuoteModel)
    assert data.price == 123.0
    assert data.close_price == 12343.0
    assert data.date == "2026-04-26"
    assert data.name == "fake"


@pytest.mark.asyncio
async def test_fetch_quote_data_raises_key_error(monkeypatch, async_client, stock_service):
    func = stock_service.fetch_quote_data
    with pytest.raises(KeyError, match="Error when fetching the price data."):
        _patch_get(
            monkeypatch,
            async_client,
            expected_url=f"{TWELVE_URL}/quote",
            expected_params={"symbol": "FAKE", "apikey": "faketoken"},
            payload={},
        )
        await func(client=async_client, symbol="FAKE", api_key="faketoken")


@pytest.mark.asyncio
async def test_fetch_date_success(monkeypatch, async_client, stock_service):
    func = stock_service.fetch_date
    response = {"close": "123.34"}
    _patch_get(
        monkeypatch,
        async_client,
        expected_url=f"{TWELVE_URL}/eod",
        expected_params={"symbol": "fake", "date": "2026-03-18", "apikey": "faketoken"},
        payload=response,
    )
    data = await func(client=async_client, symbol="fake", date="2026-03-18", api_key="faketoken")
    assert isinstance(data, FetchDatePriceModel)
    assert data.price == 123.34


@pytest.mark.asyncio
async def test_fetch_date_raises_key_error(monkeypatch, async_client, stock_service):
    func = stock_service.fetch_date
    with pytest.raises(KeyError, match="Error when fetching the date."):
        _patch_get(
            monkeypatch,
            async_client,
            expected_url=f"{TWELVE_URL}/eod",
            expected_params={"symbol": "fake", "date": "2026-03-18", "apikey": "faketoken"},
            payload={},
        )
        await func(client=async_client, symbol="fake", date="2026-03-18", api_key="faketoken")


@pytest.mark.asyncio
async def test_fetch_news_success(monkeypatch, async_client, stock_service):
    func = stock_service.fetch_news
    response = {"totalResults": 1,
                "results": [
                    {
                        "link": "https://www.fakenews.com",
                        "description": "My fake description",
                        }
                    ]
                }

    _patch_get(
        monkeypatch,
        async_client,
        expected_url=f"{NEWS_DATA_URL}/market",
        expected_params={"qInTitle": "FAKE", "apikey": "fakeapikey"},
        payload=response,
    )
    data = await func(client=async_client, symbol="FAKE", api_key="fakeapikey")
    assert isinstance(data, dict)
    assert isinstance(data["totalResults"], int)
    assert isinstance(data["articles"], list)


@pytest.mark.asyncio
async def test_fetch_news_raises_value_error(monkeypatch, async_client, stock_service):
    func = stock_service.fetch_news
    response = {"totalResults": 0,
                "results": [
                {
                    "link": "https://www.fakenews.com",
                    "description": "My fake description",
                    }
                ]
            }
    _patch_get(
        monkeypatch,
        async_client,
        expected_url=f"{NEWS_DATA_URL}/market",
        expected_params={"qInTitle": "FAKE", "apikey": "fakeapikey"},
        payload=response,
    )
    with pytest.raises(ValueError, match="News API returned 0 results."):
        await func(client=async_client, symbol="FAKE", api_key="fakeapikey")
