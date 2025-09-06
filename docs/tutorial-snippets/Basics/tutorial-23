# This file shows basic routing, data validation, and storing data in a fake database.
from datetime import datetime
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

# This dictionary acts as a simple in-memory database for demonstration.
fake_db = {}

# Pydantic model for validating and serializing item data
class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None  # Optional field

app = FastAPI()

# This endpoint responds to PUT requests at /items/{id}
# It receives an Item object, validates it, and stores it in the fake_db dictionary.
# jsonable_encoder converts the Pydantic model to a format compatible with JSON (e.g., datetime to string)
@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
    # Uncomment the line below to return the current state of the fake_db for debugging
    # return {"fake_db": fake_db}