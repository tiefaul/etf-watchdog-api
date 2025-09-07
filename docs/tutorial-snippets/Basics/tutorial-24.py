from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    """
    Dependency function that provides common query parameters.
    - q: Optional search query string
    - skip: Pagination offset (default 0)
    - limit: Pagination limit (default 100)
    Returns a dictionary with these values.
    """
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")  # Route for GET requests to /items/
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    """
    Endpoint to read items.
    Uses dependency injection to get common query parameters.
    The 'commons' argument receives the dictionary returned by common_parameters.
    """
    return commons

@app.get("/users/")  # Route for GET requests to /users/
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    """
    Endpoint to read users.
    Also uses dependency injection for common query parameters.
    """
    return commons


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# Create a dependency class instead of a function
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100) -> None:
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/class/")
async def read_class(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]): # NOTE: Shortcut write `commons: Annotated[CommonQueryParams, Depends()]`
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip:commons.skip + commons.limit]
    response.update({"items": items})
    return response