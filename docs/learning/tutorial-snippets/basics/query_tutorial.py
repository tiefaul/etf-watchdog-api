from fastapi import FastAPI, Query
import random
from typing import Annotated
from pydantic import AfterValidator

app = FastAPI()

# Example of a GET endpoint with query parameter validation using Annotated and Query
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(min_length= 3, max_length=50, pattern="^fixedquery$")] = None):
     # If q is provided and matches the pattern, it will be included in the response
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results["items"].append({"q": q})
    return results

# Example of a GET endpoint that accepts a list of query parameters with a default value
@app.get("/list/")
async def read_list(
    q: Annotated[
        list[str] | None, # Input can be a list of strings or None, if None then the default value is used.
        Query(
            title="Query output",
            description="Query string for items to search in the database, has to be more than 3 characters.",
            alias="list-query", # Example /list/?list-query=foobaritems&list-query=test
            min_length=3
            )
        ] = ["foo", "bar"] # Default value.
):
    # Returns the list of query items
    query_items = {"q": q}
    return query_items

# Example data dictionary for demonstration purposes
data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

# Custom validator function to check if an ID starts with "isbn-" or "imdb-"
def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id

# Example of using a custom validator with AfterValidator in a query parameter
@app.get("/custom-validator/")
async def read_query(
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    # If id is provided and valid, return the corresponding item
    # If id is not provided, select a random item from the data dictionary
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items())) # Picks a random (key, value) pair

    return {"id": id, "name": item}
