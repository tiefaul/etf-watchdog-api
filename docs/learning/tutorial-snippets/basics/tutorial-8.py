from typing import Annotated  # Used for type hints with extra metadata (e.g., FastAPI validation)
from fastapi import FastAPI, Path, Body  # Import FastAPI core and Path/Body for parameter validation
from pydantic import BaseModel  # BaseModel is used for data validation and parsing

app = FastAPI()  # Create a FastAPI application instance

# Pydantic model for request/response data validation
class Item(BaseModel):
    name: str  # Name of the item (required)
    description: str | None = None  # Optional description
    price: float  # Price of the item (required)
    tax: float | None = None  # Optional tax field

class User(BaseModel):
    username: str
    full_name: str | None = None # Optional full_name field

# Route for PUT requests to /items/{item_id}
# Demonstrates path/query/body parameters and response structure
@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],  # Path param with validation
    importance: Annotated[int, Body()],  # Required request body. Example of a non-required request body: importance: Annotated[int | None, Body()] = None
    q: str | None = None,  # Optional query parameter, add Body() like in line 23 if you want this to be a request body.
    item: Item | None = None,  # Optional request body (parsed as Item model)
    user: User | None = None, # # Optional request body (parsed as User model)
):
    results = {"item_id": item_id, "importance": importance}  # Start response with item_id

    if q:
        results.update({"q": q})  # type: ignore - Add query param to response if present

    if item:
        # If item is provided, check if tax is set and >= 1.0
        if item.tax is not None and item.tax >= 1.0:
            item_dict = item.model_dump()  # Convert Item model to dict
            tax_total = item.tax + item.price  # Calculate total with tax
            item_dict.update({"tax_total": tax_total})  # Add tax_total to item dict
            results.update({"item": item_dict})  # type: ignore - Add item dict to response

        results.update({"item": item})  # type: ignore - Add item as-is if no/low tax
    
    if user:
        results.update({"user": user}) # type: ignore

    return results  # Return the response as a dict (FastAPI auto-converts to JSON)