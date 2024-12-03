import json

from app.models.item_model import ItemModel
from fastapi import APIRouter, Path, Body, Header, HTTPException
from typing import Annotated

from sandbox.call_rest_service import call_boss_detail

router = APIRouter()


@router.get("/boss_detail/{company_id}")
async def boss_detail(
        company_id: str = Path(..., title="The ID of the item to create"),
        authorization: str = Header(...),
):
        # Ensure the Authorization header is present
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

        # Extract token (assuming Bearer schema)
    user_token = authorization[len("Bearer "):]
    print(user_token)

    json_string =  call_boss_detail(company_id=company_id, user_token=authorization)
    return json.loads(json_string)

