from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_get_stock():
    response = client.get("/api/stocks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["stocks"]
