# Annotated is used to add extra metadata to type hints (e.g., for validation or documentation)
from typing import Annotated

# Import FastAPI core and Body for request body handling
from fastapi import Body, FastAPI
# Import BaseModel for data validation and Field for extra field info/validation
from pydantic import BaseModel, Field

# Create a FastAPI application instance
app = FastAPI()

# Define a Pydantic model for request/response data validation
class Item(BaseModel):
    name: str  # Required field
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300  # Optional, with title and max length
    )
    price: float = Field(gt=0, description="The price must be greater than zero")  # Required, must be > 0
    tax: float | None = None  # Optional field

# Define a PUT endpoint at /items/{item_id}
# - item_id is a path parameter (int)
# - item is a required request body, validated as Item model
# - Body(embed=True) means the body will be wrapped in a key (e.g., {"item": {...}})
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    # Build the response as a dictionary
    results = {"item_id": item_id, "item": item}
    return results  # FastAPI automatically serializes the response to JSON