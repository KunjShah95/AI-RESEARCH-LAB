"""Usage endpoints"""

from typing import Annotated
from fastapi import APIRouter, Depends, Query
from app.auth.api_keys import get_current_api_key

router = APIRouter(prefix="/api", tags=["Usage"])


@router.get("/usage")
async def get_usage(
    api_key: Annotated = Depends(get_current_api_key), period: str = Query("day")
):
    from app.gateway.models import UsageRecord
    from app.database import get_db

    db = next(get_db())
    records = db.query(UsageRecord).filter_by(user_id=api_key.user_id).all()
    return {
        "total_requests": len(records),
        "total_tokens": sum(r.tokens_input + r.tokens_output for r in records),
    }
