"""Chat completions endpoint"""

from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.auth.api_keys import get_current_api_key

router = APIRouter(prefix="/v1", tags=["Chat"])


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: list[Message]
    stream: bool = False


class ChatMessage(BaseModel):
    role: str
    content: str


class Content(BaseModel):
    text: str


ContentStream = BaseModel


@router.post("/chat/completions")
async def chat_completions(
    req: ChatRequest, api_key: Annotated = Depends(get_current_api_key)
):
    if ":" not in req.model:
        raise HTTPException(status_code=400, detail="Model format: 'provider:model'")
    prov_name, model = req.model.split(":", 1)
    from app.providers.registry import get_provider
    from app.gateway.models import UsageRecord
    from app.database import get_db
    from app.crypto import decrypt_key

    db = next(get_db())
    provider = get_provider(prov_name)
    if not provider:
        raise HTTPException(status_code=400, detail="Provider not found")
    messages = [{"role": m.role, "content": m.content} for m in req.messages]
    result = await provider.chat_completions(messages, model)
    return {"choices": [{"message": {"role": "assistant", "content": result}}]}


async def chat_completions_stream(
    req: ChatRequest, api_key: Annotated = Depends(get_current_api_key)
):
    if ":" not in req.model:
        raise HTTPException(status_code=400, detail="Model format: 'provider:model'")
    prov_name, model = req.model.split(":", 1)
    from app.providers.registry import get_provider

    provider = get_provider(prov_name)
    if not provider:
        raise HTTPException(status_code=400, detail="Provider not found")
    messages = [{"role": m.role, "content": m.content} for m in req.messages]
    async for chunk in provider.chat_completions_stream(messages, model):
        yield f"data: {chunk}\n\n"
