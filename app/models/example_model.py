from pydantic import BaseModel

class ExampleModel(BaseModel):
    item_id: int
    name: str