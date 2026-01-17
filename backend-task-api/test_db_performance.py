import asyncio
import time
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from src.core.config import settings
from src.core.database import init_engines, get_async_session
from src.models.user import User
from sqlmodel import select
import uuid
from datetime import datetime
from src.api.auth import get_password_hash_sync


async def test_db_performance():
    """Test database performance with proper async operations"""
    print("Initializing database engines...")
    init_engines()

    print("Testing database connection and basic operations...")
    
    # Test getting a session and performing operations
    start_time = time.time()
    
    async for session in get_async_session():
        # Test query performance
        query_start = time.time()
        statement = select(User).limit(1)
        result = await session.execute(statement)
        users = result.scalars().all()
        query_time = time.time() - query_start
        print(f"Query execution time: {query_time:.4f}s")
        
        # Test creating a user
        create_start = time.time()
        hashed_password = get_password_hash_sync("testpassword123")  # Use sync version for testing
        
        new_user = User(
            id=uuid.uuid4(),
            email=f"perf_test_{int(time.time())}@example.com",
            password_hash=hashed_password,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        create_time = time.time() - create_start
        print(f"User creation time: {create_time:.4f}s")
        print(f"Created user with ID: {new_user.id}")
        
        total_time = time.time() - start_time
        print(f"Total operation time: {total_time:.4f}s")
        break  # Just test once


if __name__ == "__main__":
    asyncio.run(test_db_performance())