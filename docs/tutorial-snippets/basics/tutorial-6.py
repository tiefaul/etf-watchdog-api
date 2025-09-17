# Annotated is used to add metadata to function parameters, such as validation rules or documentation.
from typing import Annotated

# Import FastAPI core class, and Path/Query for parameter validation and metadata.
from fastapi import FastAPI, Path, Query

# Create a FastAPI application instance. This is the main entry point for your API.
app = FastAPI()

# Define a GET endpoint at /items/{item_id}
# The function below will be called when a GET request is made to this path.
@app.get("/items/{item_id}")
async def read_items(
    # Path parameter: item_id must be an integer >= 1. The title is used in API docs.
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)],
    # Query parameter: 'q' is optional, can be passed as ?item-query=... in the URL. Alias changes the query param name.
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    # Create a dictionary with the item_id
    results = {"item_id": item_id}
    # If a query parameter was provided, add it to the results
    if q:
        results.update({"q": q}) # type:ignore --- or results["q"] = q
    # Return the results as a JSON response
    return results