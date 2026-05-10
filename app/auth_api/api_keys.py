"""API key authentication"""

import hashlib
from datetime import datetime
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.database import get_db
from app.gateway.models import APIKey as APIKeyModel

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


async def get_current_api_key(
    authorization: Annotated[str | None, Depends(api_key_header)],
    db: Session = Depends(get_db),
) -> APIKeyModel:
    """Validate API key from Authorization header."""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="API key required"
        )

    if authorization.startswith("Bearer "):
        key = authorization[7:]
    else:
        key = authorization

    key_hash = hashlib.sha256(key.encode()).hexdigest()

    api_key = (
        db.query(APIKeyModel)
        .filter(APIKeyModel.key_hash == key_hash, APIKeyModel.is_active == True)
        .first()
    )

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired API key",
        )

    if api_key.expires_at and api_key.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="API key expired"
        )

    api_key.last_used = datetime.utcnow()
    db.commit()

    return api_key
