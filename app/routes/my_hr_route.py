import json

from fastapi import APIRouter, Path, Body, Header, HTTPException

from app.models.query_model import QueryModel
from sandbox.call_rest_service import call_boss_detail
from sandbox.tool_call_test import query_llm

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
    # print(user_token)

    json_string =  call_boss_detail(company_id, user_token)
    return json.loads(json_string)

@router.post("/chat_query/{company_id}")
async def chat_query(
        query: QueryModel = Body(...),
        company_id: str = Path(..., title="The ID of the item to create"),
        authorization: str = Header(...),
):
        # Ensure the Authorization header is present
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    user_token = authorization[len("Bearer "):]

    answer =  query_llm(query.message, company_id, authorization)
    return answer

