# Startup Script: Multi-User Todo Application

## Overview
This script helps start both the backend and frontend servers for the multi-user todo application.

## Prerequisites
- Python 3.11+ installed
- Node.js 18+ installed
- PostgreSQL server running (with Neon Serverless if deployed)

## Environment Setup

### 1. Backend Setup
```bash
# Navigate to backend directory
cd backend-task-api

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://username:password@localhost:5432/todo_app"
export JWT_SECRET_KEY="your-super-secret-jwt-key-here"
```

### 2. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend  # from project root

# Install dependencies
npm install

# Set environment variables
export NEXT_PUBLIC_API_BASE_URL="http://localhost:8000/api/v1"
export BETTER_AUTH_URL="http://localhost:3000"
```

## Starting the Application

### Method 1: Separate Terminals (Recommended)
Terminal 1 (Backend):
```bash
cd backend-task-api
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

### Method 2: Using Docker Compose
```bash
docker-compose up --build
```

### Method 3: Using Concurrently (if installed)
```bash
# From project root
concurrently "cd backend-task-api && uvicorn src.main:app --reload --port 8000" "cd frontend && npm run dev"
```

## Accessing the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/v1
- Backend Docs: http://localhost:8000/docs

## Stopping the Application
- Press Ctrl+C in each terminal running the servers
- Or use the taskkill command for background processes:
  ```bash
  taskkill /F /PID <backend_pid> /T
  taskkill /F /PID <frontend_pid> /T
  ```

## Troubleshooting

### Common Issues

#### 1. Backend won't start
- Verify virtual environment is activated
- Check that all dependencies are installed
- Ensure environment variables are properly set
- Verify database connection is available

#### 2. Frontend can't connect to backend
- Verify backend is running on the configured port
- Check that CORS settings allow frontend origin
- Ensure NEXT_PUBLIC_API_BASE_URL is set correctly

#### 3. Authentication not working
- Verify JWT_SECRET_KEY is the same in both frontend and backend
- Check that auth headers are being sent correctly
- Ensure Better Auth is properly configured

## Production Deployment

### Building for Production
Backend:
```bash
cd backend-task-api
pip install -r requirements.txt
python -m compileall src/
```

Frontend:
```bash
cd frontend
npm run build
```

### Environment Variables for Production
Ensure these variables are set in your production environment:
- `JWT_SECRET_KEY` (strong, randomly generated)
- `DATABASE_URL` (production database URL)
- `NEXT_PUBLIC_API_BASE_URL` (production backend API URL)
- `APP_ENV=production`