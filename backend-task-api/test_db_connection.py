import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from dotenv import load_dotenv
load_dotenv()

from src.core.config import settings
print(f"Database URL: {settings.DATABASE_URL}")
print(f"Async Database URL: {settings.ASYNC_DATABASE_URL}")

# Check if the URL contains the asyncpg driver
if "asyncpg" in settings.DATABASE_URL:
    print("Sync URL contains asyncpg driver")
else:
    print("Sync URL does NOT contain asyncpg driver")

if "asyncpg" in settings.ASYNC_DATABASE_URL:
    print("Async URL contains asyncpg driver")
else:
    print("Async URL does NOT contain asyncpg driver")

# Test creating the engine with a simple approach
from sqlalchemy.ext.asyncio import create_async_engine

try:
    engine = create_async_engine(settings.ASYNC_DATABASE_URL)
    print("Async engine created successfully!")
except Exception as e:
    print(f"Error creating async engine: {e}")

    # Check if asyncpg is available
    try:
        import asyncpg
        print("asyncpg is available")
    except ImportError:
        print("asyncpg is NOT available")