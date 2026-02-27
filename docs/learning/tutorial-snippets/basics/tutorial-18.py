from typing import Annotated  # Used for type annotations, especially with dependencies and forms
from fastapi import FastAPI, Form  # FastAPI is the main class, Form is for form data parsing
from pydantic import BaseModel  # Pydantic is used for data validation and parsing

# Create an instance of the FastAPI application
app = FastAPI()

# Define a Pydantic model for form data
class FormData(BaseModel):
    username: str  # Field for username (required, type: str)
    password: str  # Field for password (required, type: str)
    model_config = {"extra": "forbid"}  # Forbid extra fields not declared in the model

# Define a POST endpoint at /login/
# The @app.post decorator registers this function as handling POST requests to /login/
# The function expects form data matching the FormData model, parsed using Annotated and Form()
@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    # The function is async, which allows for non-blocking code (e.g., database calls)
    # FastAPI automatically parses form data and injects it as a Pydantic model instance
    # Returns the parsed data as JSON
    return data
