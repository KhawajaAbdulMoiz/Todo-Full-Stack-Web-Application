from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from uuid import UUID
import uuid
from datetime import datetime, timedelta
from jose import JWTError, jwt

from core.database import get_async_session
from core.config import settings
from models.user import User, UserCreate, UserRead
from models.auth import LoginCredentials
from services.auth_service import AuthService
from sqlmodel.ext.asyncio.session import AsyncSession
from core.security import create_access_token


router = APIRouter()


@router.post("/auth/register", response_model=Dict[str, Any])
async def register(user_create: UserCreate, session: AsyncSession = Depends(get_async_session)) -> Dict[str, Any]:
    auth_service = AuthService(session)

    # Create new user
    user = await auth_service.create_user(user_create)

    # Create access token
    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})

    return {
        "success": True,
        "data": {
            "user": {
                "id": str(user.id),
                "email": user.email,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat()
            },
            "token": access_token
        },
        "message": "Registration successful"
    }


@router.post("/auth/login", response_model=Dict[str, Any])
async def login(credentials: LoginCredentials, session: AsyncSession = Depends(get_async_session)) -> Dict[str, Any]:
    auth_service = AuthService(session)

    user = await auth_service.authenticate_user(credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})

    return {
        "success": True,
        "data": {
            "user": {
                "id": str(user.id),
                "email": user.email,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat()
            },
            "token": access_token
        },
        "message": "Login successful"
    }


@router.post("/auth/logout")
async def logout():
    # In a real implementation, you might want to invalidate the token
    # For now, we'll just return a success message
    return {
        "success": True,
        "message": "Logout successful"
    }