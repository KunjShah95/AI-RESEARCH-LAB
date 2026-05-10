"""API key authentication"""

from typing import Annotated
from fastapi import Depends, HTTPException, Header
from app.database import get_db
from datetime import datetime


class APIKey:
    def __init__(
        self,
        key_id: int,
        user_id: str,
        key_hash: str,
        created_at: datetime = None,
        last_used: datetime = None,
        is_active: bool = True,
    ):
        self.key_id = key_id
        self.user_id = user_id
        self.key_hash = key_hash
        self.created_at = created_at
        self.last_used = last_used
        self.is_active = is_active


async def get_current_api_key(x_api_key: str = Header(...)) -> APIKey:
    from hashlib import sha256

    db = next(get_db())
    key_hash = sha256(x_api_key.encode()).hexdigest()
    api_key = (
        db.query(APIKey)
        .filter(APIKey.key_hash == key_hash, APIKey.is_active == True)
        .first()
    )
    if not api_key:
        raise HTTPException(401, "Invalid API key")
    return api_key
