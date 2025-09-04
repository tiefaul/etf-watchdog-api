from typing import Annotated

# This example demonstrates file upload endpoints using FastAPI.
# It shows how to handle single and multiple file uploads, both as raw bytes and as UploadFile objects.

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

# Endpoint to upload a single file as bytes
@app.post("/files/")
async def create_file(file: Annotated[bytes| None, File()] = None):
    if not file:
        return {"message": "No file was sent"}
    else:
        return {"file_size": len(file)}

# Endpoint to upload a single file as an UploadFile object
@app.post("/uploadfile/")
async def create_upload_file(file: Annotated[UploadFile, File(description="A file read as UploadFile")]):
    return {"filename": file.filename}

# Endpoint to upload multiple files as a list of UploadFile objects
@app.post("/multiplefiles/")
async def upload_more_files(files: Annotated[list[UploadFile], File(description="A list of uploaded files")]):
    return {"filenames": [file.filename for file in files]}

# Root endpoint serves an HTML page with forms for file upload
@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="file" type="file" multiple>
<input type="submit">
</form>
<form action="/multiplefiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)