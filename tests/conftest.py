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


@pytest_asyncio.fixture
async def async_client():
    async with aiohttp.ClientSession() as session:
        yield session


@pytest_asyncio.fixture
async def mock_response():
    with aioresponses() as mocker:
        yield mocker
