from sqlmodel import Field, Session, SQLModel, create_engine
from typing import Annotated
from fastapi import Depends

# Database setup
DATABASE_NAME = "sqlitedb.db"
DATABASE_URL = f"sqlite:///{DATABASE_NAME}"
connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

class Stock(SQLModel, table=True):
    # __tablename__ = "items"
    id: int | None = Field(primary_key=True, default=None)
    name: str | None = None
    description: str | None = None

# This gets passed into lifespan function for FastAPI
def init_db():
    SQLModel.metadata.create_all(bind=engine)

# Dependency for getting DB session 
def get_db():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]
