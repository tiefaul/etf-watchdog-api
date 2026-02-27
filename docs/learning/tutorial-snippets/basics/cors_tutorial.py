from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000"
]

# Allow CORS for the specified origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # Allow cookies and authentication headers
    allow_methods=["*"], # Example: GET, POST, PUT
    allow_headers=["*"] # Example: Authorization, Content-Type
)

@app.get("/")
async def main():
    return {"message": "Hello World"}
