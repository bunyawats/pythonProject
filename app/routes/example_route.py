from fastapi import APIRouter
from app.models.example_model import ExampleModel

router = APIRouter()


@router.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id, "name": "Example Item"}
