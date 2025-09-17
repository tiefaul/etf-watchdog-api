
# Import Annotated for type annotations
from typing import Annotated
# Import FastAPI for creating the app, Header for extracting headers
from fastapi import FastAPI, Header
# Import BaseModel from Pydantic for data validation and parsing
from pydantic import BaseModel

# Create a FastAPI application instance
app = FastAPI()

# Define a Pydantic model for the headers you want to read
class CommonHeaders(BaseModel):
    # Required header fields
    host: str
    save_data: bool
    # Optional header fields (can be None)
    if_modified_since: str | None = None
    traceparent: str | None = None
    # List of strings for custom header (default empty list)
    x_tag: list[str] = []

# Define a GET endpoint at /items/
# The headers parameter uses the CommonHeaders model and FastAPI's Header dependency
# FastAPI will extract headers from the request and populate the model
@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    # Return the headers as a response (FastAPI will convert the model to JSON)
    return headers