from fastapi import FastAPI
from enum import Enum

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

'''
When creating path operations, you can find situations where you have a fixed path.
Like /users/me, let's say that it's to get data about the current user.
And then you can also have a path /users/{user_id} to get data about a specific user by some user ID.
Because path operations are evaluated in order, you need to make sure that the path for /users/me is declared before the one for /users/{user_id}:
Otherwise, the path for /users/{user_id} would match also for /users/me, "thinking" that it's receiving a parameter user_id with a value of "me".
'''
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# Order matters the below function will get called first.
@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]

# This will never get called because the path is the same as the one above.
@app.get("/users")
async def read_users2():
    return ["Bean", "Elfo"]

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

# Using Enum to restrict path parameter values
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# Using a path converter to capture the full path including subdirectories
@app.get("files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
