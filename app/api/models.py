"""Models list endpoint"""

from typing import Annotated
from fastapi import APIRouter, Depends
from app.auth.api_keys import get_current_api_key

router = APIRouter(prefix="/v1", tags=["Models"])


@router.get("/models")
async def list_models(api_key: Annotated = Depends(get_current_api_key)):
    from app.providers.registry import list_providers, get_provider
    from app.gateway.models import ProviderConfig

    models = []
    for name in list_providers():
        provider = get_provider(name)
        if provider and hasattr(provider, "available_models"):
            for model in provider.available_models:
                models.append({"id": f"{name}:{model}", "object": "model"})
    return {"object": "list", "data": models}
