from typing import Annotated

from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.get("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}

    if q:
        results.update({"q": q}) # type: ignore

    if item:
        if item.tax is not None and item.tax >= 1.0: # type: ignore
            item_dict = item.model_dump()
            tax_total = item.tax + item.price # type: ignore
            item_dict.update({"tax_total": tax_total})
            results.update({"item": item_dict}) # type: ignore

        else:
            results.update({"item": item}) # type: ignore

    return results