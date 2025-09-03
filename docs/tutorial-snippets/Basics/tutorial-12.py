from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}

# To return duplicate headers, convert to list
@app.get("/duplicate/")
async def duplicate_headers(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token Values": x_token}

# Example output response:
# {
    # "X-Token values": [
        # "bar",
        # "foo"
    # ]
# }