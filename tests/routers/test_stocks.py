from unittest.mock import patch, AsyncMock
import aiohttp


def test_get_stock(client):
    response = client.get("/api/stocks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "stocks" in data


def test_get_symbol(client):
    response = client.get("/api/stocks/IYW")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["symbol"] == "IYW"


def test_get_nonexistent_symbol(client):
    response = client.get("/api/stocks/fake")
    assert response.status_code == 404
    assert response.json() == {"detail": "Symbol 'fake' not found in the database."}


@patch("app.routers.stocks.stock.fetch_price", new_callable=AsyncMock)
def test_get_symbol_price(mock_fetch_price, client):
    mock_fetch_price.return_value = {
        "name": "iShares US Technology ETF",
        "price": "140.50",
        "date": "2024-05-01 16:00:00",
        "close_price": "140.00"
    }

    response = client.get("/api/stocks/IYW?price=true")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "IYW"
    assert data["stock_name"] == "iShares US Technology ETF"
    assert data["price_current"] == "140.50"
    assert data["date"] == "2024-05-01 16:00:00"
    assert data["close_price"] == "140.00"


@patch("app.routers.stocks.stock.fetch_price", new_callable=AsyncMock)
def test_get_symbol_price_key_error(mock_fetch_price, client):
    mock_fetch_price.side_effect = KeyError()

    response = client.get("/api/stocks/IYW?price=true")
    assert response.status_code == 404
    assert "Price for the stock couldn't be obtained" in response.json()["detail"]


@patch("app.routers.stocks.stock.fetch_price", new_callable=AsyncMock)
def test_get_symbol_price_network_error(mock_fetch_price, client):
    # Pass an empty request_info to avoid initialization errors with aiohttp.ClientError
    mock_fetch_price.side_effect = aiohttp.ClientError()

    response = client.get("/api/stocks/IYW?price=true")
    assert response.status_code == 502
    assert response.json()["detail"] == "Failed to connect to the external stock pricing API."


@patch("app.routers.stocks.stock.fetch_date", new_callable=AsyncMock)
def test_get_symbol_date(mock_fetch_date, client):
    mock_fetch_date.return_value = {"date": "135.00"}

    response = client.get("/api/stocks/IYW?date=2024-04-25")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "IYW"
    assert data["price_2024-04-25"] == "135.00"


def test_get_symbol_invalid_date_format(client):
    response = client.get("/api/stocks/IYW?date=04-25-2024")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid date format provided. Must be 'YYYY-MM-DD'."


@patch("app.routers.stocks.stock.fetch_date", new_callable=AsyncMock)
def test_get_symbol_date_key_error(mock_fetch_date, client):
    mock_fetch_date.side_effect = KeyError()

    response = client.get("/api/stocks/IYW?date=2024-04-25")
    assert response.status_code == 404
    assert "2024-04-25 does not appear in the stock data" in response.json()["detail"]


@patch("app.routers.stocks.stock.fetch_news", new_callable=AsyncMock)
def test_get_news(mock_fetch_news, client):
    mock_fetch_news.return_value = {
        "totalResults": 1,
        "articles": [{"link": "http://example.com", "description": "Tech stocks rally."}]
    }

    response = client.get("/api/stocks/IYW/news")
    assert response.status_code == 200
    data = response.json()
    assert data["totalResults"] == 1
    assert len(data["articles"]) == 1


@patch("app.routers.stocks.stock.fetch_news", new_callable=AsyncMock)
def test_get_news_empty(mock_fetch_news, client):
    mock_fetch_news.side_effect = ValueError()

    response = client.get("/api/stocks/IYW/news")
    assert response.status_code == 404
    assert response.json()["detail"] == "Failed to find any news for IYW."


@patch("app.routers.stocks.stock.fetch_news", new_callable=AsyncMock)
def test_get_news_network_error(mock_fetch_news, client):
    mock_fetch_news.side_effect = aiohttp.ClientError()

    response = client.get("/api/stocks/IYW/news")
    assert response.status_code == 502
    assert response.json()["detail"] == "Failed to connect to the external news API."
