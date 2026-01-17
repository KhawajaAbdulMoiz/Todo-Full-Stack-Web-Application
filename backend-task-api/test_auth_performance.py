import asyncio
import httpx
import time
from concurrent.futures import ThreadPoolExecutor
import threading


async def test_single_request(client, url, payload, request_type="register"):
    """Test a single authentication request"""
    try:
        if request_type == "register":
            response = await client.post(url, json=payload)
        elif request_type == "login":
            response = await client.post(url, json=payload)
        
        print(f"{request_type.title()} Response Status: {response.status_code}")
        if response.status_code == 200:
            print(f"{request_type.title()} Success: {response.json()['message']}")
        else:
            print(f"{request_type.title()} Error: {response.text}")
        return response
    except Exception as e:
        print(f"Request failed: {str(e)}")
        return None


async def test_concurrent_requests():
    """Test concurrent authentication requests to check for performance issues"""
    base_url = "http://127.0.0.1:8000/api/v1"
    
    # Test data
    test_users = [
        {"email": "test1@example.com", "password": "password123"},
        {"email": "test2@example.com", "password": "password123"},
        {"email": "test3@example.com", "password": "password123"},
    ]
    
    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
        print("Testing concurrent registration requests...")
        start_time = time.time()
        
        # Register multiple users concurrently
        register_tasks = []
        for i, user_data in enumerate(test_users):
            task = test_single_request(
                client, 
                f"{base_url}/auth/register", 
                user_data, 
                "register"
            )
            register_tasks.append(task)
        
        register_results = await asyncio.gather(*register_tasks, return_exceptions=True)
        register_time = time.time() - start_time
        
        print(f"\nRegistration completed in {register_time:.2f} seconds")
        
        # Now test login for the first user
        print("\nTesting login request...")
        login_start = time.time()
        login_payload = {"email": "test1@example.com", "password": "password123"}
        login_response = await test_single_request(
            client, 
            f"{base_url}/auth/login", 
            login_payload, 
            "login"
        )
        login_time = time.time() - login_start
        
        print(f"Login completed in {login_time:.2f} seconds")


async def test_single_register():
    """Test a single registration request"""
    base_url = "http://127.0.0.1:8000/api/v1"
    
    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
        print("Testing single registration request...")
        start_time = time.time()
        
        payload = {"email": "performance_test@example.com", "password": "securepassword123"}
        response = await test_single_request(
            client, 
            f"{base_url}/auth/register", 
            payload, 
            "register"
        )
        
        end_time = time.time()
        print(f"Single registration completed in {end_time - start_time:.2f} seconds")
        
        if response and response.status_code == 200:
            # Test login with the same credentials
            print("\nTesting login with registered user...")
            login_start = time.time()
            
            login_payload = {"email": "performance_test@example.com", "password": "securepassword123"}
            login_response = await test_single_request(
                client, 
                f"{base_url}/auth/login", 
                login_payload, 
                "login"
            )
            
            login_end = time.time()
            print(f"Login completed in {login_end - login_start:.2f} seconds")


if __name__ == "__main__":
    print("Starting authentication performance tests...")
    print("=" * 50)
    
    # Test single request first
    asyncio.run(test_single_register())
    
    print("\n" + "=" * 50)
    print("Starting concurrent request tests...")
    asyncio.run(test_concurrent_requests())