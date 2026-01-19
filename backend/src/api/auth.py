from fastapi import APIRouter, HTTPException, status, Depends
from contextlib import asynccontextmanager
from src.core.database import AsyncSessionLocal
from src.services.auth_service import AuthService
from src.models.user import UserCreate, UserRead
from src.core.security import create_access_token, blacklist_token, verify_token
from datetime import timedelta, datetime
from typing import Dict, Any
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.models.auth import LoginRequest, RegisterRequest

router = APIRouter()
security = HTTPBearer()


@router.post("/auth/register", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest):
    email = payload.email
    password = payload.password

    """
    Register a new user with email and password.

    Args:
        email: User's email address
        password: User's password (will be hashed)

    Returns:
        A dictionary containing the access token, token type, and user info
    """
    async with AsyncSessionLocal() as session:
        auth_service = AuthService(session)

        # Check if user already exists
        existing_user = await auth_service.get_user_by_email(email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )

        # Create new user
        user_create = UserCreate(email=email, password=password)
        user = await auth_service.create_user(user_create)

        # Create access token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )

        return {
            "token": access_token,
            "user": {
                "id": str(user.id),
                "email": user.email
            }
        }


@router.post("/auth/login")
async def login(payload: LoginRequest):
    async with AsyncSessionLocal() as session:
        auth_service = AuthService(session)

        user = await auth_service.authenticate(payload.email, payload.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=timedelta(minutes=30)
        )

        return {
            "token": access_token,
            "user": {
                "id": str(user.id),
                "email": user.email
            }
        }

@router.post("/auth/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Logout endpoint to invalidate token.

    Args:
        credentials: Bearer token from Authorization header
    """
    token = credentials.credentials

    # Get token expiration to store in blacklist
    payload = verify_token(token)
    if payload:
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            expires_at = datetime.utcfromtimestamp(exp_timestamp)
            await blacklist_token(token, expires_at)

    return {"message": "Successfully logged out"}