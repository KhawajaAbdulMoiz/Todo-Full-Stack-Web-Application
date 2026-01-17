from datetime import datetime, timedelta
from typing import Optional, Union
from sqlmodel.ext.asyncio.session import AsyncSession
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.core.config import settings
from src.models.user import User
from src.models.token_blacklist import TokenBlacklist, TokenBlacklistCreate
from sqlmodel import select
import uuid


# Initialize JWT token scheme
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)  # 30 minutes as per AUTH_IMPLEMENTATION.md

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.BETTER_AUTH_SECRET, algorithm="HS256")
    return encoded_jwt


async def is_token_blacklisted(token: str) -> bool:
    """Check if a token is in the blacklist."""
    from src.core.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        statement = select(TokenBlacklist).where(TokenBlacklist.token == token)
        result = await session.exec(statement)
        blacklisted_token = result.first()
        return blacklisted_token is not None


async def blacklist_token(token: str, expires_at: datetime):
    """Add a token to the blacklist."""
    from src.core.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        # Check if token is already blacklisted
        statement = select(TokenBlacklist).where(TokenBlacklist.token == token)
        result = await session.exec(statement)
        existing = result.first()

        if not existing:
            # Create new blacklist entry
            blacklist_record = TokenBlacklist(token=token, expires_at=expires_at)
            session.add(blacklist_record)
            await session.commit()


async def cleanup_expired_tokens():
    """Remove expired tokens from the blacklist."""
    from src.core.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        # Find tokens that have expired
        statement = select(TokenBlacklist).where(TokenBlacklist.expires_at < datetime.utcnow())
        result = await session.exec(statement)
        expired_tokens = result.all()

        # Delete expired tokens
        for token in expired_tokens:
            await session.delete(token)

        await session.commit()


def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return payload
    except JWTError:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    token = credentials.credentials

    # Check if token is blacklisted
    if await is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Fetch the user from the database
    from src.core.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        try:
            user_uuid = uuid.UUID(user_id)
            statement = select(User).where(User.id == user_uuid)
            result = await session.exec(statement)
            user = result.first()

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return user
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID in token",
                headers={"WWW-Authenticate": "Bearer"},
            )