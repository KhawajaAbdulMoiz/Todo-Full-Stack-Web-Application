import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Manually load the .env file
from dotenv import load_dotenv
load_dotenv('.env')

print(f"Environment DATABASE_URL: {os.environ.get('DATABASE_URL')}")

# Now import the settings
from core.config import Settings
settings_obj = Settings()

print(f"Settings DATABASE_URL: {settings_obj.DATABASE_URL}")
print(f"Settings ASYNC_DATABASE_URL: {settings_obj.ASYNC_DATABASE_URL}")