from app.services.stock_service import StockService
from app.main import app
from fastapi.testclient import TestClient
from sqlmodel.pool import StaticPool
from sqlmodel import (
        create_engine,
        SQLModel,
        Session
        )
from app.services.app_state import get_db_session
import pytest
import requests
from aioresponses import aioresponses
import aiohttp
import pytest_asyncio


@pytest.fixture(autouse=True)
def disable_network_calls(monkeypatch):
    def stunted_get():
        raise RuntimeError("Network access not allowed during testing!")
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: stunted_get())


@pytest.fixture
def stock_service():
    return StockService()


# Async test client
@pytest_asyncio.fixture
async def async_client():
    async with aiohttp.ClientSession() as session:
        yield session


@pytest_asyncio.fixture
async def mock_response():
    with aioresponses() as mocker:
        yield mocker


# FastAPI test client
@pytest.fixture
def client(db_session: Session):
    def get_session_override():
        return db_session

    app.dependency_overrides[get_db_session] = get_session_override

    with TestClient(app) as client:
        yield client
        app.dependency_overrides.clear()


# Database test session
@pytest.fixture
def db_session():
    engine = create_engine(
            "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
            )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
