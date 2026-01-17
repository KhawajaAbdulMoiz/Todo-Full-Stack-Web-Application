import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Change to the directory containing the .env file
os.chdir(os.path.dirname(__file__))

# Explicitly load the .env file
from dotenv import load_dotenv
load_dotenv('.env')

print(f"Current working directory: {os.getcwd()}")
print(f"Environment DATABASE_URL: {os.environ.get('DATABASE_URL', 'NOT SET')}")

# Import after loading environment
from src.core.config import settings
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=(settings.APP_ENV == "development")
    )