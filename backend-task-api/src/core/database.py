from sqlmodel import create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import asyncio

from core.config import settings


# Engines will be initialized later
async_engine = None
sync_engine = None
AsyncSessionLocal = None


def init_engines():
    global async_engine, sync_engine, AsyncSessionLocal

    # Async engine for database - use the proper async URL directly
    async_engine = create_async_engine(
        settings.ASYNC_DATABASE_URL,
        echo=(settings.APP_ENV == "development"),  # Only show SQL in development
        pool_size=20,  # Increase pool size for better concurrency
        max_overflow=30,  # Allow additional connections when needed
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=300,  # Recycle connections every 5 minutes
    )

    # Sync engine (for Alembic migrations)
    sync_engine = create_engine(
        settings.DATABASE_URL,
        echo=(settings.APP_ENV == "development"),  # Only show SQL in development
        pool_pre_ping=True,  # Verify connections before use
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
    from models.user import User  # noqa: F401
    from models.task import Task  # noqa: F401
    from sqlmodel import SQLModel

    # Initialize engines if not already done
    if async_engine is None:
        init_engines()

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    # Initialize engines if not already done
    if AsyncSessionLocal is None:
        init_engines()

    async with AsyncSessionLocal() as session:
        yield session