"""Provider management endpoints"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.auth.api_keys import get_current_api_key

router = APIRouter(prefix="/api", tags=["Providers"])


@router.get("/providers")
async def list_providers(api_key: Annotated = Depends(get_current_api_key)):
    from app.providers.registry import list_providers as list_reg

    return {"providers": list_reg()}
