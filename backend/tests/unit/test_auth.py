import pytest
import asyncio
from httpx import AsyncClient
from src.main import app
from src.core.config import settings
from src.core.database import create_db_and_tables, AsyncSessionLocal
from src.models.user import User
from src.models.token_blacklist import TokenBlacklist
from sqlmodel import select


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_register_endpoint():
    """Test the registration endpoint."""
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.post(
            f"{settings.API_V1_STR}/auth/register",
            data={
                "email": "test@example.com",
                "password": "testpassword123"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_login_endpoint():
    """Test the login endpoint."""
    # First register a user
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        # Register user
        await ac.post(
            f"{settings.API_V1_STR}/auth/register",
            data={
                "email": "login_test@example.com",
                "password": "testpassword123"
            }
        )
        
        # Try to login
        response = await ac.post(
            f"{settings.API_V1_STR}/auth/login",
            data={
                "email": "login_test@example.com",
                "password": "testpassword123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_logout_endpoint():
    """Test the logout endpoint."""
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        # Register user
        register_response = await ac.post(
            f"{settings.API_V1_STR}/auth/register",
            data={
                "email": "logout_test@example.com",
                "password": "testpassword123"
            }
        )
        
        # Extract token from registration
        token = register_response.json()["access_token"]
        
        # Logout
        response = await ac.post(
            f"{settings.API_V1_STR}/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "Successfully logged out"}