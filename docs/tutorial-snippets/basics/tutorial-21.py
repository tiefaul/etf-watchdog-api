from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

# This FastAPI example demonstrates:
# - Basic routing and endpoint creation
# - Custom error handling with HTTPException and user-defined exceptions
# - Returning custom headers and status codes
# - Registering exception handlers for custom exceptions

app = FastAPI()


# Dictionary to store item data
items = {"foo": "The Foo Wrestlers"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    # Returns the item if found, otherwise raises a 404 error with a custom header and message
    if item_id not in items:
        raise HTTPException(
            status_code=404, 
            detail="You are dumb",
            headers={"X-Error": "There goes my error"},
        )   
    return {"item": items[item_id]}


# Custom exception class for demonstration
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    # Handles UnicornException, returns a playful message and status code 418
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )

@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    # Raises UnicornException if name is "yolo", otherwise returns the unicorn name
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}