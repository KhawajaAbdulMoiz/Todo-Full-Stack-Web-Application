@echo off
cd /d "E:\FullStackTodoApp\backend-task-api"
python -c "
import sys
import os
sys.path.insert(0, '.')

from dotenv import load_dotenv
load_dotenv('.env')

from src.core.config import settings
import uvicorn
print('Starting server...')
uvicorn.run('src.main:app', host=settings.SERVER_HOST, port=settings.SERVER_PORT, reload=(settings.APP_ENV == 'development'))
"
pause