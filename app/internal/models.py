from sqlmodel import Field, SQLModel, UniqueConstraint


class Stock(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    ticker_symbol: str = Field(unique=True, index=True)
    company_name: str | None = None
    currency: str | None = None


class StockPrice(SQLModel, table=True):
    __table_args__ = (
            UniqueConstraint("stock_id", "price_date"),
            )
    id: int | None = Field(primary_key=True, default=None)
    stock_id: int = Field(foreign_key="stock.id")
    price_date: str = Field(index=True)
    close_price: int | None = None


class NewsArticles(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    title: str | None = None
    url: str
    summary: str | None = None

