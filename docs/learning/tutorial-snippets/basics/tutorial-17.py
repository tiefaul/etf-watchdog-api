from typing import Annotated  # Used for type annotations, especially with dependencies and forms
from fastapi import FastAPI, Form  # FastAPI is the main class, Form is for form data parsing

# Create an instance of the FastAPI application
app = FastAPI()

# Define a POST endpoint at /login/
# The @app.post decorator registers this function as handling POST requests to /login/
@app.post("/login/")
async def login(
    username: Annotated[str, Form()],  # Annotated tells FastAPI to expect this field from a form
    password: Annotated[str, Form()]   # Same for password
):
    # The function is async, which allows for non-blocking code (e.g., database calls)
    # FastAPI automatically parses form data and injects it into the function arguments
    # Returns a JSON response with the username
    return {"username": username}