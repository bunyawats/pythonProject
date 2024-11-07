# app/routes/item_route.py
from app.models.item_model import ItemModel
from fastapi import APIRouter, Path, Body, Header, HTTPException
from typing import Annotated

router = APIRouter()


@router.post("/items/{item_id}")
async def create_item(
        item_id: int = Path(..., title="The ID of the item to create"),
        item: ItemModel = Body(...),
        api_key: Annotated[str | None, Header(convert_underscores=False)] = None,
):
    print( api_key)
    if api_key != "your-expected-api-key":
        raise HTTPException(status_code=403, detail="Invalid API Key")

    return {
        "item_id": item_id,
        "item": item.model_dump(),
        "api_key": api_key
    }
