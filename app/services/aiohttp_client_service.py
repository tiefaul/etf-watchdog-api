import aiohttp
from socket import AF_INET

SIZE_POOL_AIOHTTP = 100

class HttpClient:
    """Manager for the aiohttp ClientSession"""
    def __init__(self):
        self.aiohttp_client: aiohttp.ClientSession | None = None

    def start_http_client(self):
        if self.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=2)
            connector = aiohttp.TCPConnector(family=AF_INET, limit_per_host=SIZE_POOL_AIOHTTP)
            self.aiohttp_client = aiohttp.ClientSession(
                timeout=timeout,
                connector=connector,
            )

    async def stop_http_client(self):
        if self.aiohttp_client:
            await self.aiohttp_client.close()
            self.aiohttp_client = None

    def get_session(self) -> aiohttp.ClientSession:
        if self.aiohttp_client is None:
            raise RuntimeError("HttpClient has not initalized")
        return self.aiohttp_client
