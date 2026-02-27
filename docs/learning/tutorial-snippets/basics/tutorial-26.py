from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []}
}

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item:Item):
    """
    This is not recommended for partial updates.
    That means that if you want to update the item `bar` using `PUT` with a body containing:
    ```json
    {
        "name": "Barz",
        "price": 3,
        "description": None,
    }
    ```
    because it doesn't include the already stored attribute "tax": 20.2, the input model would take the default value of "tax": 10.5.
    And the data would be saved with that "new" tax of 10.5. View the Patch request for a workaround on this topic.
    """
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded

@app.patch("/items/{item_id}", response_model=Item)
async def update_items(item_id: str, item: Item):
    """
    This is the recommended way of doing partial updates.
    This avoids the `default` mistakes written in the previous
    `PUT` method.
    """
    stored_item_data = items[item_id] # Retrieve the stored data
    stored_item_model = Item(**stored_item_data) # Unpack the data and put it in the pydantic model `Item`
    update_data = item.model_dump(exclude_unset=True) # Generate a dictionary without the default values from the input model (using exclude_unset). This way you can update only the values actually set by the user, instead of overriding values already stored with default values in your model.
    update_item = stored_item_model.model_copy(update=update_data) # Create a copy of the stored model, updating the attributes with the received partial updates (using the update param)
    items[item_id] = jsonable_encoder(update_item) # Convert the copied model to something that can be stored into you DB (example using the `jsonable_encoder`)
    return update_item
