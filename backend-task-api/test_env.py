import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv(dotenv_path='.env')

# Print the raw environment variable
print("Raw DATABASE_URL from environment:", os.environ.get('DATABASE_URL'))

# Also check if we're in the right directory
print("Current working directory:", os.getcwd())

# Try to load from a different path
import pathlib
env_path = pathlib.Path(__file__).parent / '.env'
print("Env file exists at root:", env_path.exists())
if env_path.exists():
    with open(env_path, 'r') as f:
        print("Content of .env file:")
        print(f.read())