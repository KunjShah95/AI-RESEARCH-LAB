"""Admin API - user management and stats"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta


router = APIRouter()


class UserStats(BaseModel):
    total_users: int
    active_users: int
    papers_searched: int
    papers_generated: int
    projects_created: int


class UserInfo(BaseModel):
    id: str
    email: str
    name: str
    role: str
    created_at: datetime
    last_active: datetime


class SystemStats(BaseModel):
    uptime: str
    total_api_calls: int
    papers_in_db: int
    cache_hit_rate: float


# Demo data
admin_stats = {
    "total_users": 42,
    "active_users": 15,
    "papers_searched": 1250,
    "papers_generated": 89,
    "projects_created": 67,
    "total_api_calls": 45678,
    "papers_in_db": 5432,
    "cache_hit_rate": 0.78,
}


@router.get("/stats", response_model=UserStats)
async def get_user_stats():
    """Get user statistics"""
    return UserStats(**admin_stats)


@router.get("/system", response_model=SystemStats)
async def get_system_stats():
    """Get system statistics"""
    return SystemStats(
        uptime="14 days, 3 hours",
        total_api_calls=admin_stats["total_api_calls"],
        papers_in_db=admin_stats["papers_in_db"],
        cache_hit_rate=admin_stats["cache_hit_rate"],
    )


@router.get("/users", response_model=List[UserInfo])
async def list_users(role: Optional[str] = None):
    """List all users"""
    users = [
        UserInfo(
            id="1",
            email="admin@researchlab.com",
            name="Admin User",
            role="admin",
            created_at=datetime.utcnow() - timedelta(days=30),
            last_active=datetime.utcnow(),
        ),
        UserInfo(
            id="2",
            email="researcher@researchlab.com",
            name="Researcher",
            role="researcher",
            created_at=datetime.utcnow() - timedelta(days=15),
            last_active=datetime.utcnow() - timedelta(hours=2),
        ),
    ]
    if role:
        users = [u for u in users if u.role == role]
    return users


@router.post("/users/{user_id}/role")
async def update_user_role(user_id: str, role: str):
    """Update user role"""
    if role not in ["reader", "researcher", "admin", "auditor"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    return {"user_id": user_id, "role": role, "updated": True}


@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    """Delete a user"""
    return {"message": f"User {user_id} deleted"}
