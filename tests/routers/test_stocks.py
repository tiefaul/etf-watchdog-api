from unittest.mock import patch, AsyncMock
import aiohttp
from fastapi.testclient import TestClient
from sqlmodel import Session
from backend.internal.models import (
        Stock,
        StockNews,
        StockPrice
        )
from datetime import date
from backend.routers.stocks import get_latest_trading_day


def test_get_all_stocks_success(client: TestClient, db_session: Session):
    statement = Stock(ticker_symbol="IYW")
    db_session.add(statement)
    response = client.get("/api/etfs")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "IYW" in data


def test_get_all_stocks_raises_http_404(client: TestClient):
    response = client.get("/api/etfs")
    assert response.status_code == 404
    assert response.json() == {"detail": "No stocks found in the database."}


@patch("backend.routers.stocks.stock.fetch_price", new_callable=AsyncMock)
def test_post_stock_success(mock_fetch_price, client: TestClient):
    mock_fetch_price.return_value = {
        "name": "iShares US Technology ETF",
        "price": "140.50",
        "date": "2024-05-01 16:00:00",
        "close_price": 140.00
    }

    response = client.post("/api/etfs", json={"ticker_symbol": "IYW"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["id"], int)
    assert data["ticker_symbol"] == "IYW"
    assert data["company_name"] == "iShares US Technology ETF"
    assert isinstance(data["currency"], str)


@patch("backend.routers.stocks.stock.fetch_price", new_callable=AsyncMock)
def test_post_stock_raises_http_404_on_client_response_error(mock_fetch_price, client: TestClient):
    mock_fetch_price.side_effect = aiohttp.ClientResponseError(history=(), request_info=None) # type: ignore

    response = client.post("/api/etfs", json={"ticker_symbol": "FAKE"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Stock could not be found. Please ensure you are using the correct ticker symbol."}


@patch("backend.routers.stocks.stock.fetch_price", new_callable=AsyncMock)
def test_post_stock_raises_http_404_on_key_error(mock_fetch_price, client: TestClient):
    mock_fetch_price.side_effect = KeyError()

    response = client.post("/api/etfs", json={"ticker_symbol": "FAKE"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Stock could not be found. Please ensure you are using the correct ticker symbol."}


def test_post_stock_raises_http_409(client: TestClient, db_session: Session):
    statement = Stock(ticker_symbol="IYW")
    db_session.add(statement)

    response = client.post("/api/etfs", json={"ticker_symbol": "IYW"})
    assert response.status_code == 409
    assert isinstance(response.json(), dict)
    assert response.json() == {"detail": "Ticker symbol already exists."}


def test_get_symbol_success(client: TestClient, db_session: Session):
    statement = Stock(ticker_symbol="AAPL", company_name="Apple INC", currency="USD")
    db_session.add(statement)

    response = client.get("/api/etfs/AAPL")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert isinstance(data["id"], int)
    assert data["ticker_symbol"] == "AAPL"
    assert data["company_name"] == "Apple INC"
    assert data["currency"] == "USD"


def test_get_symbol_raises_http_404(client: TestClient):
    response = client.get("/api/etfs/FAKE")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticker symbol not found in the database."}


def test_get_symbol_price_success(client: TestClient, db_session: Session):
    latest_trading_day = get_latest_trading_day(date.today()).isoformat()
    add_stock_statement = Stock(ticker_symbol="AAPL")
    db_session.add(add_stock_statement)
    db_session.commit()
    add_stock_price_statement = StockPrice(price_date=latest_trading_day, close_price=200.10, stock_id=add_stock_statement.id)
    db_session.add(add_stock_price_statement)

    response = client.get("/api/etfs/AAPL/price")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["ticker_symbol"] == "AAPL"
    assert data["price_date"] == latest_trading_day
    assert data["close_price"] == 200.10


def test_get_symbol_price_raises_http_404(client: TestClient):
    response = client.get("/api/etfs/AAPL/price")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticker symbol not found in the database."}


@patch("backend.routers.stocks.stock.fetch_price", new_callable=AsyncMock)
def test_get_symbol_price_raises_http_404_on_fetch_price(mock_fetch_price, client: TestClient, db_session: Session):
    mock_fetch_price.side_effect = KeyError()

    add_stock_statement = Stock(ticker_symbol="AAPL")
    db_session.add(add_stock_statement)

    response = client.get("api/etfs/AAPL/price")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Price could not be obtained. Stock market could have been closed on date: {date.today().isoformat()}"}


def test_get_symbol_price_by_date_success(client: TestClient, db_session: Session):
    add_stock_statement = Stock(ticker_symbol="AAPL")
    db_session.add(add_stock_statement)
    db_session.commit()
    add_stock_price_statement = StockPrice(price_date="2025-10-13", close_price=110.12, stock_id=add_stock_statement.id)
    db_session.add(add_stock_price_statement)

    response = client.get("/api/etfs/AAPL/price?price_date=2025-10-13")
    assert response.status_code == 200

    data = response.json()
    assert data["price_date"] == "2025-10-13"
    assert data["close_price"] == 110.12
    assert data["ticker_symbol"] == "AAPL"


@patch("backend.routers.stocks.stock.fetch_date", new_callable=AsyncMock)
def test_get_symbol_price_by_date_raises_http_404(mock_fetch_date, client: TestClient, db_session: Session):
    mock_fetch_date.side_effect = aiohttp.ClientResponseError(history=(), request_info=None) # type: ignore

    add_stock_statement = Stock(ticker_symbol="FAKE")
    db_session.add(add_stock_statement)

    response = client.get("/api/etfs/FAKE/price?price_date=2025-04-25")
    assert response.status_code == 404
    assert response.json() == {"detail": "Could not find a price on that date. This could have been a weekend, holiday, or sometime in the future."}


@patch("backend.routers.stocks.stock.fetch_news", new_callable=AsyncMock)
def test_get_news_success(mock_fetch_news, client: TestClient):
    mock_fetch_news.return_value = {
        "totalResults": 1,
        "articles": [{"link": "http://example.com", "description": "Tech stocks rally."}]
    }

    response = client.get("/api/etfs/IYW/news")
    assert response.status_code == 200
    data = response.json()
    assert data["totalResults"] == 1
    assert len(data["articles"]) == 1


@patch("backend.routers.stocks.stock.fetch_news", new_callable=AsyncMock)
def test_get_news_raises_value_error(mock_fetch_news, client: TestClient):
    mock_fetch_news.side_effect = ValueError()

    response = client.get("/api/etfs/IYW/news")
    assert response.status_code == 404
    assert response.json() == {"detail": "Failed to find any news for IYW."}


@patch("backend.routers.stocks.stock.fetch_news", new_callable=AsyncMock)
def test_get_news_raises_client_error(mock_fetch_news, client: TestClient):
    mock_fetch_news.side_effect = aiohttp.ClientError()

    response = client.get("/api/etfs/IYW/news")
    assert response.status_code == 502
    assert response.json() == {"detail": "Failed to connect to the external news API."}
