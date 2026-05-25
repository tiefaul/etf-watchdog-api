from sqlmodel import Field, SQLModel


class Stock(SQLModel, table=True):
    # __tablename__ = "items"
    id: int | None = Field(primary_key=True, default=None)
    ticker_symbol: str
    company_name: str | None = None
    currency: str | None = None


# class StockPrice(SQLModel, table=True):
#     id: int | None = Field(primary_key=True, default=None)



