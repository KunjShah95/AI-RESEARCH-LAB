"""Authentication and authorization"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt


class Role(str, Enum):
    READER = "reader"
    RESEARCHER = "researcher"
    ADMIN = "admin"
    AUDITOR = "auditor"


class User(BaseModel):
    id: str
    email: str
    name: str
    role: Role = Role.READER
    org_id: Optional[str] = None


class TokenData(BaseModel):
    user_id: str
    email: str
    role: Role
    exp: datetime


SECRET_KEY = "research-lab-secret-key-change-in-production"
ALGORITHM = "HS256"


def create_access_token(
    user: User, expires_delta: timedelta = timedelta(hours=24)
) -> str:
    """Create JWT access token"""
    expire = datetime.utcnow() + expires_delta
    to_encode = {
        "user_id": user.id,
        "email": user.email,
        "role": user.role.value,
        "exp": expire,
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> Optional[TokenData]:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(**payload)
    except jwt.InvalidTokenError:
        return None


def check_permission(user: User, required_role: Role) -> bool:
    """Check if user has required role"""
    role_hierarchy = {
        Role.AUDITOR: 4,
        Role.ADMIN: 3,
        Role.RESEARCHER: 2,
        Role.READER: 1,
    }
    return role_hierarchy.get(user.role, 0) >= role_hierarchy.get(required_role, 0)
