# Quickstart Guide: Multi-User Todo Web Application

## Overview
This guide provides step-by-step instructions to set up and run the multi-user todo web application locally. The application consists of a Next.js frontend and a FastAPI backend with Neon Serverless PostgreSQL database.

## Prerequisites
- Node.js 18+ installed
- Python 3.11+ installed
- PostgreSQL client tools (for database operations)
- Git for version control

## Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set Up Environment Variables
Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration
DATABASE_URL="postgresql://username:password@localhost:5432/todo_app"

# Better Auth Configuration
BETTER_AUTH_SECRET="your-super-secret-jwt-key-here"
BETTER_AUTH_URL="http://localhost:3000"

# Neon PostgreSQL Configuration (if using Neon)
NEON_DATABASE_URL="your-neon-database-url"

# Application Configuration
APP_ENV="development"
PORT=8000
FRONTEND_URL="http://localhost:3000"
```

For production, ensure you use strong, randomly generated secrets.

## Backend Setup (FastAPI)

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Database
```bash
# Run database migrations
alembic upgrade head
```

### 5. Start Backend Server
```bash
uvicorn src.main:app --reload
```

The backend will be available at `http://localhost:8000`.

## Frontend Setup (Next.js)

### 1. Navigate to Frontend Directory
```bash
cd frontend  # From project root
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Start Frontend Development Server
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## Running the Application

### 1. Start Backend First
Ensure the backend is running at `http://localhost:8000` before starting the frontend.

### 2. Start Frontend
Start the frontend at `http://localhost:3000`.

### 3. Access the Application
Open your browser and navigate to `http://localhost:3000`.

## Key Features Walkthrough

### 1. User Registration
- Navigate to `/register`
- Enter your email and password
- Account will be created and you'll be logged in

### 2. User Login
- Navigate to `/login`
- Enter your credentials
- JWT token will be stored securely

### 3. Task Management
- After authentication, access the dashboard
- Create, read, update, and delete tasks
- Toggle task completion status

### 4. Security Features
- All API requests include JWT authentication
- Users can only access their own tasks
- Unauthorized requests return 401 status

## Development Commands

### Backend Commands
```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src

# Format code
black src/

# Lint code
flake8 src/
```

### Frontend Commands
```bash
# Run tests
npm test

# Run tests in watch mode
npm run test:watch

# Build for production
npm run build

# Lint code
npm run lint

# Format code
npm run format
```

## Database Migrations

### Creating New Migrations
```bash
# From backend directory
alembic revision --autogenerate -m "Description of changes"
```

### Applying Migrations
```bash
# Apply all pending migrations
alembic upgrade head

# Downgrade to a specific version
alembic downgrade <revision-id>
```

## Troubleshooting

### Common Issues

#### 1. Backend won't start
- Verify virtual environment is activated
- Check that all dependencies are installed
- Ensure environment variables are set correctly

#### 2. Frontend can't connect to backend
- Verify backend is running on the configured port
- Check that CORS settings allow frontend origin
- Ensure API endpoints in frontend match backend routes

#### 3. Authentication not working
- Verify JWT secret is the same in both frontend and backend
- Check that auth headers are being sent correctly
- Ensure Better Auth is properly configured

#### 4. Database connection errors
- Verify database URL is correct
- Check that database server is running
- Ensure required database extensions are installed

## Testing the Application

### 1. Unit Tests
Run backend unit tests:
```bash
cd backend
pytest tests/unit/
```

Run frontend unit tests:
```bash
cd frontend
npm run test
```

### 2. Integration Tests
Test the integration between components:
```bash
cd backend
pytest tests/integration/
```

### 3. End-to-End Tests
Test complete user workflows:
```bash
cd frontend
npm run test:e2e
```

## Production Deployment

### Building for Production
```bash
# Backend
cd backend
pip install -r requirements.txt
python -m compileall src/

# Frontend
cd frontend
npm run build
```

### Environment Variables for Production
Ensure these variables are set in your production environment:
- `BETTER_AUTH_SECRET` (strong, randomly generated)
- `DATABASE_URL` (production database URL)
- `FRONTEND_URL` (production frontend URL)
- `APP_ENV=production`