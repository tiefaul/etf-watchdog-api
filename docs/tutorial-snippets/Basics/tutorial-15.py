# Import FastAPI for building the API, BaseModel and EmailStr for data validation, Any for type hints
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Any

# Create a FastAPI application instance
app = FastAPI()

# Define a Pydantic model for an item
class Item(BaseModel):
    name: str  # Required field
    description: str | None = None  # Optional field
    price: float  # Required field
    tax: float | None = None  # Optional field
    tags: list[str] = []  # List of tags, default empty

# POST endpoint to create an item
# The request body is parsed as an Item model
# Returns the created item
@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item

# GET endpoint to retrieve a list of items
# Returns a hardcoded list of Item objects
@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]

# Pydantic model for user input (includes password)
class UserIn(BaseModel):
    username: str
    password: str  # Password should be hashed in real apps
    email: EmailStr  # Validates email format
    full_name: str | None = None

# Pydantic model for user output (excludes password)
class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

# POST endpoint to create a user
# Accepts UserIn model, returns UserOut model (password is excluded from response)
@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user


# Define a Pydantic model for an item
class ItemsExample(BaseModel):
    name: str  # Required field
    description: str | None = None  # Optional field
    price: float  # Required field
    tax: float = 10.5  # Default value for tax

# Dictionary to simulate a database of items
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}

# GET endpoint to retrieve only the name and description of an item
# response_model_include limits the response to only specified fields
@app.get(
    "/items/{item_id}/name",
    response_model=ItemsExample,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]

# GET endpoint to retrieve item data excluding the tax field
# response_model_exclude omits specified fields from the response
@app.get("/items/{item_id}/public", response_model=ItemsExample, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]