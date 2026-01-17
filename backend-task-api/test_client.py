import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi.testclient import TestClient
from src.main import app

# Create a test client
client = TestClient(app)

# Test the root endpoint
response = client.get("/")
print(f"Root endpoint status: {response.status_code}")
print(f"Root endpoint response: {response.json()}")

# Test the registration endpoint with a new email
response = client.post("/api/v1/auth/register", json={
    "email": "newuser@example.com",
    "password": "testpassword"
})
print(f"Registration endpoint status: {response.status_code}")
print(f"Registration endpoint response: {response.text}")

# Test the login endpoint
response = client.post("/api/v1/auth/login", json={
    "email": "newuser@example.com",
    "password": "testpassword"
})
print(f"Login endpoint status: {response.status_code}")
print(f"Login endpoint response: {response.text}")