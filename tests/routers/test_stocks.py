from unittest.mock import patch, AsyncMock
import aiohttp
from fastapi.testclient import TestClient
from sqlmodel import Session
from backend.internal.models import (
        Stock,
        StockNews,
        StockPrice
        )


def test_get_all_stocks_success(client: TestClient, db_session: Session):
    statement = Stock(ticker_symbol="IYW")
    db_session.add(statement)
    response = client.get("/api/stocks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "stocks" in data
    assert "IYW" in data["stocks"]


def test_get_all_stocks_raises_http_404(client: TestClient):
    response = client.get("/api/stocks")
    assert response.status_code == 404
    assert response.json() == {"detail": "No stocks were found."}


@patch("backend.routers.stocks.stock.fetch_price", new_callable=AsyncMock)
def test_post_stock_success(mock_fetch_price, client: TestClient):
    mock_fetch_price.return_value = {
        "name": "iShares US Technology ETF",
        "price": "140.50",
        "date": "2024-05-01 16:00:00",
        "close_price": 140.00
    }

    response = client.post("/api/stocks", json={"ticker_symbol": "IYW"})
    data = response.json()

    assert isinstance(data["id"], int)
    assert data["ticker_symbol"] == "IYW"
    assert data["company_name"] == "iShares US Technology ETF"
    assert isinstance(data["currency"], str)


@patch("backend.routers.stocks.stock.fetch_price", new_callable=AsyncMock)
def test_post_stock_raises_http_404(mock_fetch_price, client: TestClient):
    mock_fetch_price.side_effect = aiohttp.ClientError()

    response = client.post("/api/stocks", json={"ticker_symbol": "FAKE"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Stock could not be found. Please ensure you are using the correct ticker symbol."}


def test_post_stock_raises_http_409(client: TestClient, db_session: Session):
    statement = Stock(ticker_symbol="IYW")
    db_session.add(statement)
    response = client.post("/api/stocks", json={"ticker_symbol": "IYW"})
    assert response.json() == {"detail": "Ticker symbol already exists."}


def test_get_symbol_success(client: TestClient):
    response = client.get("/api/stocks/IYW")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["symbol"] == "IYW"


def test_get_symbol_raises_http_404(client: TestClient):
    response = client.get("/api/stocks/fake")
    assert response.status_code == 404
    assert response.json() == {"detail": "Symbol 'fake' not found in the database."}


@patch("backend.routers.stocks.stock.fetch_price", new_callable=AsyncMock)
def test_get_symbol_price_success(mock_fetch_price, client: TestClient):
    mock_fetch_price.return_value = {
        "name": "iShares US Technology ETF",
        "price": "140.50",
        "date": "2024-05-01 16:00:00",
        "close_price": 140.00
    }

    response = client.get("/api/stocks/IYW?price=true")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "IYW"
    assert data["stock_name"] == "iShares US Technology ETF"
    assert data["price_current"] == "140.50"
    assert data["date"] == "2024-05-01 16:00:00"
    assert data["close_price"] == 140.00


@patch("backend.routers.stocks.stock.fetch_price", new_callable=AsyncMock)
def test_get_symbol_price_raises_key_error(mock_fetch_price, client: TestClient):
    mock_fetch_price.side_effect = KeyError()

    response = client.get("/api/stocks/IYW?price=true")
    assert response.status_code == 404
    assert response.json() == {"detail": "Price for the stock couldn't be obtained. Either the price isn't listed or API key is invalid. Symbol: IYW"}


@patch("backend.routers.stocks.stock.fetch_price", new_callable=AsyncMock)
def test_get_symbol_price_raises_client_error(mock_fetch_price, client):
    # Pass an empty request_info to avoid initialization errors with aiohttp.ClientError
    mock_fetch_price.side_effect = aiohttp.ClientError()

    response = client.get("/api/stocks/IYW?price=true")
    assert response.status_code == 502
    assert response.json() == {"detail": "Failed to connect to the external stock pricing API."}


@patch("backend.routers.stocks.stock.fetch_date", new_callable=AsyncMock)
def test_get_symbol_date_success(mock_fetch_date, client: TestClient):
    mock_fetch_date.return_value = {"date": "135.00"}

    response = client.get("/api/stocks/IYW?date=2024-04-25")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "IYW"
    assert data["price_2024-04-25"] == "135.00"


def test_get_symbol_date_raises_http_400(client: TestClient):
    response = client.get("/api/stocks/IYW?date=04-25-2024")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid date format provided. Must be 'YYYY-MM-DD'."}


@patch("backend.routers.stocks.stock.fetch_date", new_callable=AsyncMock)
def test_get_symbol_date_raises_key_error(mock_fetch_date, client):
    mock_fetch_date.side_effect = KeyError()

    response = client.get("/api/stocks/IYW?date=2024-04-25")
    assert response.status_code == 404
    assert response.json() == {"detail": "2024-04-25 does not appear in the stock data. Possibly tried to request data from the future or on a weekend/holiday."}


@patch("backend.routers.stocks.stock.fetch_news", new_callable=AsyncMock)
def test_get_news_success(mock_fetch_news, client: TestClient):
    mock_fetch_news.return_value = {
        "totalResults": 1,
        "articles": [{"link": "http://example.com", "description": "Tech stocks rally."}]
    }

    response = client.get("/api/stocks/IYW/news")
    assert response.status_code == 200
    data = response.json()
    assert data["totalResults"] == 1
    assert len(data["articles"]) == 1


@patch("backend.routers.stocks.stock.fetch_news", new_callable=AsyncMock)
def test_get_news_raises_value_error(mock_fetch_news, client: TestClient):
    mock_fetch_news.side_effect = ValueError()

    response = client.get("/api/stocks/IYW/news")
    assert response.status_code == 404
    assert response.json() == {"detail": "Failed to find any news for IYW."}


@patch("backend.routers.stocks.stock.fetch_news", new_callable=AsyncMock)
def test_get_news_raises_client_error(mock_fetch_news, client: TestClient):
    mock_fetch_news.side_effect = aiohttp.ClientError()

    response = client.get("/api/stocks/IYW/news")
    assert response.status_code == 502
    assert response.json() == {"detail": "Failed to connect to the external news API."}
