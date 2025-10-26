from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .internal.database import Item, SessionDep, init_db
from contextlib import asynccontextmanager
from sqlmodel import select

# FastAPI app with lifespan event to initialize the database
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

class ItemCreate(BaseModel):
    name: str
    description: str

class ItemResponse(BaseModel):
    id: int
    name: str
    description: str

# Create a new item
@app.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: SessionDep):
    db_item = Item.model_validate(item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Find item based off of the item name
@app.get("/items/{name}", response_model=ItemResponse)
def read_item(name: str, db: SessionDep):
    item_name = select(Item).where(Item.name == name) # Query to find item by name
    item = db.exec(item_name).first() # Get the first result from the query
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Delete item based off of the item id
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: SessionDep):
    db_item = db.get(Item, item_id) # Get item by primary key (item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        db.delete(db_item)
        db.commit()
    return {"message": f"{item_id} has been removed"}
