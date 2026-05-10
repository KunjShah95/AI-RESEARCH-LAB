"""API key management endpoints"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.auth.api_keys import get_current_api_key

router = APIRouter(prefix="/api", tags=["Keys"])


class CreateKeyRequest(BaseModel):
    name: str
    provider: str
    api_key: str


@router.post("/keys")
async def create_key(
    req: CreateKeyRequest, api_key: Annotated = Depends(get_current_api_key)
):
    from app.crypto import encrypt_key
    from app.database import get_db

    db = next(get_db())
    return {"status": "ok"}
