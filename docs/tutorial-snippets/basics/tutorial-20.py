from typing import Annotated  # Used for advanced type hints and dependency injection
from fastapi import FastAPI, File, Form, UploadFile  # File and Form for request parsing, UploadFile for file handling

# Create FastAPI app instance
app = FastAPI()

# Define a POST endpoint for file uploads and form data
@app.post("/files/")
async def create_file(
    file: Annotated[bytes, File()],         # Accepts a file as raw bytes
    fileb: Annotated[UploadFile, File()],   # Accepts a file as an UploadFile object (provides .filename, .content_type, .read())
    token: Annotated[str, Form()],          # Accepts a form field named 'token'
):
    # The function is async, allowing for non-blocking file operations
    # FastAPI parses the incoming multipart/form-data request and injects the files and form fields
    # You can access fileb.filename, fileb.content_type, and use await fileb.read() for file contents
    # The response is returned as JSON
    return {
        "file_size": len(file),                 # Size of the first uploaded file (in bytes)
        "token": token,                         # Value of the form field 'token'
        "fileb_content_type": fileb.content_type, # Content type of the second uploaded file
    }