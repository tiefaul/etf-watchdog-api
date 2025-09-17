
# Import Annotated for type annotations, Cookie for cookie extraction, FastAPI for the app
from typing import Annotated
from fastapi import Cookie, FastAPI
# BaseModel from Pydantic is used for data validation and parsing
from pydantic import BaseModel

# Create a FastAPI application instance
app = FastAPI()

# Define a Pydantic model for the cookies you want to read
class Cookies(BaseModel):
    # This cookie is required
    session_id: str
    # These cookies are optional (can be None)
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None

# Define a GET endpoint at /items/
# The cookies parameter uses the Cookies model and FastAPI's Cookie dependency
# FastAPI will automatically extract cookies from the request and populate the model
@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    # Return the cookies as a response (FastAPI will convert the model to JSON)
    return cookies