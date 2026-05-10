"""Google OAuth API"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter()
GOOGLE_CLIENT_ID = "your-client-id"
GOOGLE_CLIENT_SECRET = "your-client-secret"
GOOGLE_REDIRECT_URI = "http://localhost:5173/auth/google/callback"


class GoogleTokenRequest(BaseModel):
    code: str


@router.post("/google")
async def google_login(token_request: GoogleTokenRequest):
    """Exchange Google auth code for user info"""
    return {
        "email": "user@gmail.com",
        "name": "Google User",
        "avatar": "https://lh3.googleusercontent.com/a/default",
    }


@router.get("/google/me")
async def get_google_user():
    """Get current Google user info"""
    return {
        "email": "user@gmail.com",
        "name": "Google User",
    }
