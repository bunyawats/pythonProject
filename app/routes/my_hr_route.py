import json

from fastapi import APIRouter, Path, Body, Header, HTTPException
from sandbox.call_rest_service import call_boss_detail

router = APIRouter()


# company_id = "eb2f4f30-edaf-11ee-a69a-c7680edc0e47"
# user_token = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzY2hlbWEiOiJkYm8iLCJlbmNvZGUiOiIyIiwic3ViIjoiQXV0aCIsImNvbXBhbnlOYW1lIjoi4Lia4Lij4Li04Lip4Lix4LiXIOC4oeC4suC4ouC5gOC4reC4iuC4reC4suC4o-C5jCDguIjguLPguIHguLHguJQiLCJkYk5hbWUiOiJNWUhSUExVUyIsInJvbGVzIjpbIlVTRVIiXSwid29ya2FyZWEiOiJUS1ciLCJpc3MiOiJDb21wdXRlciBTY2llbmNlIENvcnBvcmF0aW9uIExpbWl0ZWQiLCJ6bWxvZ2luIjoiZmFsc2UiLCJyb2xlX2xldmVsIjoiNiIsImVtcGxveWVlaWQiOiIxMDAwMDA4MiIsImJyYW5jaCI6Im15aHIiLCJlbXBfcG9zaXRpb24iOiIwOTciLCJ1c2VyX3JvbGUiOiJBbGwiLCJ1aWQiOiIxMDAwMDA4MiIsImNvbXBhbnlpZCI6IjEwMCIsImFjdG9yaWQiOiIxMDAwMDA4MiIsImxhbmciOiJ0aCIsImFkIjoiZmFsc2UiLCJmaXJzdGxvZ2luIjoiZmFsc2UiLCJ1cmxfbXlociI6Imh0dHA6Ly9ocnBsdXMtc3RkLm15aHIuY28udGgvaHIiLCJhcHBfbmFtZSI6Im15aHIiLCJyZWdpb25hbGx0eSI6IkVORyIsInRva2VuX3plZW1lIjoiIiwidXNlcl9sZXZlbCI6Ik1ZSFIiLCJmdWxsbmFtZSI6IuC4meC4suC4ouC4reC4nuC4tOC4o-C4seC4leC4meC5jCAg4LiX4LiU4Liq4Lit4LiaIiwiY29taWQiOiIiLCJqb2IiOiIwOTctMjQ2OSIsInVzZXIiOiJteWhyIiwiem1fdXNlciI6IiIsInVzZXJuYW1lIjoibXlociIsIm1lbWJlcmlkIjoiIn0.R70ZQ1_HPA1pq-jeyxD-K4eKZKLYVIg2jmFDhenQjQc"

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

    query = "What is 3 * 12? Also, what is 11 + 49?"
    json_string =  call_boss_detail(query, company_id, user_token)
    return json.loads(json_string)

