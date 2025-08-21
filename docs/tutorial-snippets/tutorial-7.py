# Annotated is used for parameter metadata, Literal restricts values to specific choices.
from typing import Annotated, Literal

# Import FastAPI for API creation, Query for query parameter handling.
from fastapi import FastAPI, Query
# Import BaseModel and Field from Pydantic for data validation and settings.
from pydantic import BaseModel, Field

# Create the FastAPI app instance.
app = FastAPI()


# Define a Pydantic model for query parameters. This helps with validation and documentation.
class FilterParams(BaseModel):
    # Forbid extra fields not defined in the model (strict validation)
    model_config = {"extra": "forbid"}
    
    # limit: integer, default 100, must be >0 and <=100
    limit: int = Field(100, gt=0, le=100)
    # offset: integer, default 0, must be >=0
    offset: int = Field(0, ge=0)
    # order_by: only allows 'created_at' or 'updated_at', default is 'created_at'
    order_by: Literal["created_at", "updated_at"] = "created_at"
    # tags: list of strings, default empty list
    tags: list[str] = []


# Define a GET endpoint at /items/
# The query parameters are parsed into a FilterParams model instance.
@app.get("/items/")
async def read_items(
    # The query parameters are automatically validated and parsed into example_query
    example_query: Annotated[FilterParams, Query()]
):
    # Return the parsed and validated query parameters as JSON
    return example_query