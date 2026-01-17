import os
import sys
sys.path.append('.')

from dotenv import load_dotenv
load_dotenv()

from src.core.config import settings

print(f"DATABASE_URL from settings: {settings.DATABASE_URL}")
print(f"ASYNC_DATABASE_URL from settings: {settings.ASYNC_DATABASE_URL}")