# Import FastAPI for building APIs
from fastapi import FastAPI
# Import BaseModel for data validation, HttpUrl for URL validation
from pydantic import BaseModel, HttpUrl

# Create a FastAPI application instance
app = FastAPI()

# Pydantic model for an image, with URL validation
class Image(BaseModel):
    url: HttpUrl  # Validates that the value is a proper URL
    name: str     # Name of the image

# Pydantic model for an item in the store
class Item(BaseModel):
    name: str  # Required field
    description: str | None = None  # Optional field
    price: float  # Required field
    tax: float | None = None  # Optional field
    tags: list[str] = [] # or set[str] = set()  # List of tags, defaults to empty list
    image: list[Image] | None = None  # Optional list of images

# Pydantic model for an offer, which can include multiple items
class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]  # List of Item objects

# Endpoint to update an item by its ID
# - item_id is a path parameter (int)
# - item is a required request body, validated as Item model
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results  # FastAPI automatically serializes the response to JSON

# Endpoint to create a new offer
# - Expects an Offer object in the request body
@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

# Example endpoint: accepts a dictionary with int keys and float values
@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights