from sqlmodel import create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import asyncio

# Async engine for Neon PostgreSQL
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to False in production
)

# Sync engine (for Alembic migrations)
sync_engine = create_engine(
    settings.DATABASE_URL.replace("+asyncpg", ""),
    echo=True,  # Set to False in production
)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def create_db_and_tables():
    """Create database tables"""
    from src.models.user import User  # noqa: F401
    from src.models.task import Task  # noqa: F401
    from src.models.token_blacklist import TokenBlacklist  # noqa: F401
    from sqlmodel import SQLModel

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session