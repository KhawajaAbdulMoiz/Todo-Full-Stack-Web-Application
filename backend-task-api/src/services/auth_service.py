from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt

from models.user import User, UserCreate
from core.config import settings
from core.security import verify_password, get_password_hash
from core.database import get_async_session


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password.
        
        Args:
            email: User's email address
            password: User's plain text password
            
        Returns:
            User object if authentication is successful, None otherwise
        """
        # Find user by email
        user_statement = select(User).where(User.email == email)
        result = await self.session.execute(user_statement)
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.password_hash):
            return None
        
        return user

    async def create_user(self, user_create: UserCreate) -> User:
        """
        Create a new user with the provided details.
        
        Args:
            user_create: User creation details
            
        Returns:
            Created User object
        """
        # Check if user already exists
        existing_user_statement = select(User).where(User.email == user_create.email)
        result = await self.session.execute(existing_user_statement)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )

        # Hash the password
        hashed_password = get_password_hash(user_create.password)

        # Create new user
        user = User(
            email=user_create.email,
            password_hash=hashed_password,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.
        
        Args:
            email: User's email address
            
        Returns:
            User object if found, None otherwise
        """
        user_statement = select(User).where(User.email == email)
        result = await self.session.execute(user_statement)
        user = result.scalar_one_or_none()
        return user