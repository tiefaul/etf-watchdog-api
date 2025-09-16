from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()

def fake_hash_password(password: str):
    return "fakehashed" + password

# This sets up OAuth2 password bearer authentication.
# The token will be extracted from requests using this scheme.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# User model: represents a user with username, email, full_name, and disabled fields.
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

# Class that takes in the User model above and adds a hashed_password field
class UserInDB(User):
    hashed_password: str

# This function grabs a username from a db (fake_users_db) and unpacks it into the UserInDB model.
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# This function simulates decoding a token and creates a User object.
def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

# This async function gets a token from the request using oauth2_scheme.
# It then decodes the token using fake_decode_token and returns the User object.
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# This async function depends on get_current_user to get the current user.
# It checks if the user is disabled and raises an error if so.
# Otherwise, it returns the current user.
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# API endpoint: /tokenUrl
# This endpoint is used to get a token.
# It verifies the username and password, and if valid, returns a token.
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)

    # Verify password
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

# API endpoint: /users/me
# Depends on get_current_user, so it returns the current user (decoded from token).
@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user
