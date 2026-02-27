
# Import FastAPI for building the API, BaseModel and EmailStr for data validation, Union for type hints
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Union


# Create a FastAPI application instance
app = FastAPI()


# Base user model for shared fields
class UserBase(BaseModel):
    username: str
    email: EmailStr  # Validates email format
    full_name: str | None = None  # Optional field


# Output model for user (inherits from UserBase, no password)
class UserOut(UserBase):
    pass


# Input model for user creation (includes password)
class UserIn(UserBase):
    password: str


# Model for user as stored in the database (with hashed password)
class UserInDB(UserBase):
    hashed_password: str


# Fake password hashing function (for demonstration only)
def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


# Fake function to simulate saving a user (prints to console)
def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)  # Hash the password
    # Create a UserInDB instance with all fields from user_in and the hashed password
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print("User saved.... not really")
    return user_in_db


# POST endpoint to create a user
# Accepts UserIn model, returns UserOut model (password is excluded from response)
@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
#-------------------------------------------------------------------------------#

# Pydantic model for an item
class Item(BaseModel):
    name: str
    description: str


# List of items (simulates a database)
items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]


# GET endpoint to retrieve all items
@app.get("/items/", response_model=list[Item])
async def read_items():
    return items
#-------------------------------------------------------------------------------#

# Base model for items with a type
class BaseItem(BaseModel):
    description: str
    type: str


# Model for car items (inherits from BaseItem)
class CarItem(BaseItem):
    type: str = "car"


# Model for plane items (inherits from BaseItem, adds size)
class PlaneItem(BaseItem):
    type: str = "plane"
    size: int


# Dictionary of items with different types (car, plane)
items2 = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


# GET endpoint to retrieve an item by ID
# Returns either a PlaneItem or CarItem depending on the data. Place most specific class first.
@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items2[item_id]
#-------------------------------------------------------------------------------#

# GET endpoint to retrieve keyword weights as a dictionary
@app.get("/keyword-weights/", response_model=dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}