"""Webhooks API - webhook management for search alerts"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uuid
import httpx


router = APIRouter()


class WebhookCreate(BaseModel):
    url: str
    name: str
    event: str  # "new_paper", "search_match", "citation_alert"
    filters: Optional[dict] = None


class WebhookUpdate(BaseModel):
    url: Optional[str] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None


class Webhook(BaseModel):
    id: str
    url: str
    name: str
    event: str
    filters: Optional[dict]
    is_active: bool
    user_id: str
    created_at: datetime
    last_triggered: Optional[datetime]
    trigger_count: int


# In-memory storage
webhooks_db: dict = {}


@router.get("/", response_model=List[Webhook])
async def list_webhooks(user_id: str = "default"):
    """List user's webhooks"""
    return [w for w in webhooks_db.values() if w.user_id == user_id]


@router.post("/", response_model=Webhook)
async def create_webhook(webhook: WebhookCreate, user_id: str = "default"):
    """Create a new webhook"""
    webhook_id = str(uuid.uuid4())

    new_webhook = Webhook(
        id=webhook_id,
        url=webhook.url,
        name=webhook.name,
        event=webhook.event,
        filters=webhook.filters,
        is_active=True,
        user_id=user_id,
        created_at=datetime.utcnow(),
        last_triggered=None,
        trigger_count=0,
    )

    webhooks_db[webhook_id] = new_webhook
    return new_webhook


@router.get("/{webhook_id}", response_model=Webhook)
async def get_webhook(webhook_id: str, user_id: str = "default"):
    """Get webhook by ID"""
    webhook = webhooks_db.get(webhook_id)
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    if webhook.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return webhook


@router.put("/{webhook_id}", response_model=Webhook)
async def update_webhook(
    webhook_id: str, update: WebhookUpdate, user_id: str = "default"
):
    """Update a webhook"""
    webhook = webhooks_db.get(webhook_id)
    if not webhook or webhook.user_id != user_id:
        raise HTTPException(status_code=404, detail="Webhook not found")

    if update.url:
        webhook.url = update.url
    if update.name:
        webhook.name = update.name
    if update.is_active is not None:
        webhook.is_active = update.is_active

    return webhook


@router.delete("/{webhook_id}")
async def delete_webhook(webhook_id: str, user_id: str = "default"):
    """Delete a webhook"""
    webhook = webhooks_db.get(webhook_id)
    if not webhook or webhook.user_id != user_id:
        raise HTTPException(status_code=404, detail="Webhook not found")

    del webhooks_db[webhook_id]
    return {"message": "Webhook deleted"}


@router.post("/{webhook_id}/test")
async def test_webhook(webhook_id: str, user_id: str = "default"):
    """Test a webhook"""
    webhook = webhooks_db.get(webhook_id)
    if not webhook or webhook.user_id != user_id:
        raise HTTPException(status_code=404, detail="Webhook not found")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                webhook.url, json={"event": "test", "webhook_id": webhook_id}
            )
        return {"success": response.status_code < 400, "status": response.status_code}
    except Exception as e:
        return {"success": False, "error": str(e)}


async def trigger_webhooks(event: str, data: dict):
    """Trigger all matching webhooks"""
    for webhook in webhooks_db.values():
        if webhook.is_active and webhook.event == event:
            try:
                async with httpx.AsyncClient() as client:
                    await client.post(webhook.url, json=data)
                webhook.last_triggered = datetime.utcnow()
                webhook.trigger_count += 1
            except Exception as e:
                print(f"Webhook trigger error: {e}")
