from fastapi.testclient import TestClient
from app.main import app
from app.services.aiohttp_client_service import HttpClient
import pytest

client = TestClient(app)


def test_get_stock():
    response = client.get("/api/stocks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["stocks"]


@pytest.mark.asyncio
async def test_get_symbol():
    with TestClient(app) as client:
        response = client.get("/api/stocks/IYW")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert data["symbol"]


@pytest.mark.asyncio
async def test_get_nonexistent_symbol():
    with TestClient(app) as client:
        response = client.get("api/stocks/fake")
        assert response.status_code == 404
        assert response.json() == {"detail": "Symbol 'fake' not found in the database."}


@pytest.mark.asyncio
async def test_get_symbol_price():
    with TestClient(app) as client:
        response = client.get("/api/stocks/IYW?price=true")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert data["stock_name"]
        assert data["price_current"]
        assert data["date"]
        assert data["close_price"]


@pytest.mark.asyncio
async def test_get_nonexistent_symbol_price():
    with TestClient(app) as client:
        response = client.get("/api/stocks/")
