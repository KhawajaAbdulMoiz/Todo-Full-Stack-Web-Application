import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from src.core.config import settings
from src.core.database import init_engines, get_async_session
from src.models.user import User
from sqlmodel import select
import uuid

async def test_db():
    # Initialize engines
    init_engines()

    # Get a session
    async for session in get_async_session():
        # Try to query users
        statement = select(User)
        result = await session.execute(statement)
        users = result.scalars().all()
        print(f"Found {len(users)} users")

        # Try to create a user
        new_user = User(
            id=uuid.uuid4(),
            email="test@example.com",
            password_hash="hashed_password",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        print(f"Created user with ID: {new_user.id}")
        break  # Just test once

if __name__ == "__main__":
    from datetime import datetime
    asyncio.run(test_db())