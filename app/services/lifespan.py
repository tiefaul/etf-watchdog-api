import aiohttp
from socket import AF_INET
from sqlmodel import Session, SQLModel, create_engine
# from typing import Annotated
# from fastapi import Depends


class HttpClient:
    """Manager for the aiohttp ClientSession"""
    def __init__(self):
        self.aiohttp_client: aiohttp.ClientSession | None = None
        self.size_pool_aiohttp = 100

    def start_http_client(self):
        if self.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=2)
            connector = aiohttp.TCPConnector(family=AF_INET, limit_per_host=self.size_pool_aiohttp)
            self.aiohttp_client = aiohttp.ClientSession(
                timeout=timeout,
                connector=connector,
            )

    async def stop_http_client(self) -> None:
        if self.aiohttp_client:
            await self.aiohttp_client.close()
            self.aiohttp_client = None

    def get_session(self) -> aiohttp.ClientSession:
        if self.aiohttp_client is None:
            raise RuntimeError("HttpClient has not initalized")
        return self.aiohttp_client


class DatabaseManager:
    DATABASE_NAME = "sqlitedb.db"
    DATABASE_URL = f"sqlite:///{DATABASE_NAME}"
    connect_args = {"check_same_thread": False}
    engine = create_engine(
            DATABASE_URL,
            echo=True, # remove True for prod
            connect_args=connect_args
            )

    # This gets passed into lifespan function for FastAPI
    @classmethod
    def init_db(cls):
        return SQLModel.metadata.create_all(bind=cls.engine)

    # Dependency for getting DB session 
    @classmethod
    def get_db(cls):
        if cls.engine is None:
            raise RuntimeError("Database engine was not initalized.")
        with Session(cls.engine) as session:
            yield session

# SessionDep = Annotated[Session, Depends(get_db)]
