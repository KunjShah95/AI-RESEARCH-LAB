"""Auth API endpoints"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from app.auth import User, Role, create_access_token, verify_token
from app import auth as auth_module

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: User


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Login endpoint (mock for now)"""
    user = User(
        id="user-1", email=request.email, name="Researcher", role=Role.RESEARCHER
    )
    token = create_access_token(user)
    return LoginResponse(access_token=token, token_type="bearer", user=user)


@router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user info"""
    token_data = verify_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    return User(
        id=token_data.user_id,
        email=token_data.email,
        name=token_data.email.split("@")[0],
        role=token_data.role,
    )
