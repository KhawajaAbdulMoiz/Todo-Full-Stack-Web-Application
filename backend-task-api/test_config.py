import os
import sys
sys.path.append('src')

# Force reload the config module
if 'src.core.config' in sys.modules:
    del sys.modules['src.core.config']

from src.core.config import settings

print(f"DATABASE_URL from settings: {settings.DATABASE_URL}")
print(f"ASYNC_DATABASE_URL from settings: {settings.ASYNC_DATABASE_URL}")