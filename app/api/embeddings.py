"""Embeddings endpoint"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.auth.api_keys import get_current_api_key

router = APIRouter(prefix="/v1", tags=["Embeddings"])


class EmbeddingRequest(BaseModel):
    model: str
    input: str | list[str]


@router.post("/embeddings")
async def create_embeddings(
    req: EmbeddingRequest, api_key: Annotated = Depends(get_current_api_key)
):
    if ":" not in req.model:
        raise HTTPException(status_code=400, detail="Model format: 'provider:model'")
    prov_name, model = req.model.split(":", 1)
    from app.gateway.models import ProviderConfig
    from app.providers.registry import get_provider
    from app.crypto import decrypt_key
    from app.database import get_db

    db = next(get_db())
    config = (
        db.query(ProviderConfig)
        .filter_by(provider=prov_name, user_id=api_key.user_id)
        .first()
    )
    if not config:
        raise HTTPException(status_code=400, detail="Provider not configured")
    provider = get_provider(prov_name)
    if not provider:
        raise HTTPException(status_code=400, detail="Provider not found")
    provider._api_key = decrypt_key(config.encrypted_key)
    result = await provider.embeddings(req.input, model)
    return {
        "object": "list",
        "data": [{"embedding": e, "index": i} for i, e in enumerate(result)],
    }
