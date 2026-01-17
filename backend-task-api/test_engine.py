from sqlalchemy.ext.asyncio import create_async_engine

# Test async engine creation
DATABASE_URL = "postgresql+asyncpg://neondb_owner:npg_dEbFVL24hvel@ep-rough-bonus-ahihz9pa-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

try:
    async_engine = create_async_engine(DATABASE_URL)
    print("Async engine created successfully!")
except Exception as e:
    print(f"Error creating async engine: {e}")
    
    # Try with different URL format
    alt_url = DATABASE_URL.replace("channel_binding=require", "")
    try:
        async_engine = create_async_engine(alt_url)
        print("Async engine created with alternative URL!")
    except Exception as e2:
        print(f"Alternative URL also failed: {e2}")