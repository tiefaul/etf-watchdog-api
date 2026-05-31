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

class Stock(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    ticker_symbol: str = Field(unique=True, index=True)
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


class StockPublic(SQLModel):
    ticker_symbol: str


class StockPrice(SQLModel, table=True):
    __table_args__ = (
            UniqueConstraint("stock_id", "price_date"),
            )
    id: int | None = Field(primary_key=True, default=None)
    stock_id: int = Field(foreign_key="stock.id")
    price_date: str = Field(index=True)
    close_price: int | None = None
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        ))


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
    DatabaseManager.init_db()
