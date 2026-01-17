from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from typing import Dict, Any
from uuid import UUID
import uuid
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.exc import IntegrityError
import asyncio

from core.database import get_async_session
from core.config import settings
from models.user import User, UserCreate, UserRead
from models.auth import LoginCredentials
from sqlmodel.ext.asyncio.session import AsyncSession


# Configure password hashing with faster algorithm for better performance
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()


# def verify_password_sync(plain_password: str, hashed_password: str) -> bool:
#     # bcrypt hard limit
#     safe_password = plain_password.encode("utf-8")[:72]
#     return pwd_context.verify(safe_password, hashed_password)


# async def verify_password(plain_password: str, hashed_password: str) -> bool:
#     # Run password verification in a thread pool to avoid blocking the event loop
#     loop = asyncio.get_event_loop()
#     return await loop.run_in_executor(None, verify_password_sync, plain_password, hashed_password)


# def get_password_hash_sync(password: str) -> str:
#     password = password.encode("utf-8")

#     # bcrypt hard limit
#     if len(password) > 72:
#         password = password[:72]

#     return pwd_context.hash(password)



# def get_password_hash(password: str) -> str:
#     safe_password = password.encode("utf-8")[:72]
#     return pwd_context.hash(safe_password)

def get_password_hash(password: str) -> str:
    # passlib handles encoding + bcrypt limits internally
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


@router.post("/auth/register", response_model=Dict[str, Any])
async def register(user_create: UserCreate, session: AsyncSession = Depends(get_async_session)) -> Dict[str, Any]:
    # Check if user already exists
    existing_user_statement = select(User).where(User.email == user_create.email)
    result = await session.execute(existing_user_statement)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    # Hash the password asynchronously to avoid blocking the event loop
    hashed_password = get_password_hash(user_create.password)


    # Create new user
    user = User(
        id=uuid.uuid4(),
        email=user_create.email,
        password_hash=hashed_password,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    # Create access token
    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})

    return {
        "success": True,
        "data": {
            "user": {
                "id": str(user.id),  # Convert UUID to string
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
    # Find user by email
    user_statement = select(User).where(User.email == credentials.email)
    result = await session.execute(user_statement)
    user = result.scalar_one_or_none()

    if not user or not verify_password(credentials.password, user.password_hash):
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