# app/api/rules.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/rules/{rule_id}")
def get_rule(rule_id: int):
    # Example rule fetching logic
    return {"rule_id": rule_id, "name": "Example Rule"}
