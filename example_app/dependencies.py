from fastapi import Header, HTTPException
from typing_extensions import Annotated

# Dependency to validate a custom header token
# This can be used to secure certain routes
async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

# Dependency to validate a query parameter get_token_header
# This can be used to secure the entire application
async def get_query_token(token:str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
