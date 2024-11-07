# app/models/item_model.py
from pydantic import BaseModel

class ItemModel(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
