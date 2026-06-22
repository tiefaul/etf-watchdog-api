from sqlmodel import (
        FetchedValue,
        Field,
        SQLModel,
        UniqueConstraint,
        TIMESTAMP,
        Column,
        text
        )
from datetime import datetime
from ..services.lifespan import DatabaseManager


"""Stock Models"""
class StockBase(SQLModel):
    ticker_symbol: str = Field(unique=True, index=True)


class Stock(StockBase, table=True):
    id: int | None = Field(primary_key=True, default=None)
    company_name: str | None = None
    currency: str | None = None
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        ))
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue(),
        ))


# raises 422
class StockCreate(StockBase):
    pass


class StockPublic(StockBase):
    id: int
    ticker_symbol: str
    company_name: str | None = None
    currency: str | None = None


"""Stock Price Models"""
class StockPriceBase(SQLModel):
    price_date: str = Field(index=True)
    close_price: float


class StockPrice(StockPriceBase, table=True):
    __table_args__ = (
            UniqueConstraint("stock_id", "price_date"),
            )
    id: int | None = Field(primary_key=True, default=None)
    stock_id: int | None = Field(foreign_key="stock.id", default=None)
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        ))


class StockPricePublic(StockPriceBase):
    """Place ticker symbol in here because I do not want the SQLModel to create a entry in the db."""
    ticker_symbol: str


"""Stock News Models"""
class NewsArticle(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    title: str | None = None
    url: str = Field(unique=True)
    summary: str | None = None
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        ))


class StockNews(SQLModel, table=True):
    __table_args__ = (
            UniqueConstraint("stock_id", "article_id"),
            )
    id: int | None = Field(primary_key=True, default=None)
    stock_id: int = Field(foreign_key="stock.id")
    article_id: int = Field(foreign_key="newsarticle.id")


# Future proof Users for now
class User(SQLModel, table = True):
    id: int = Field(primary_key=True)
    email: str = Field(unique=True)
    username: str
    password_hash: str
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        ))


if __name__ == "__main__":
    # For testing purposes. Run `uv run python -m backend.internal.models`
    DatabaseManager.init_db()
