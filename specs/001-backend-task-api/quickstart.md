# Quickstart Guide: Backend API & Database (Task Management)

## Overview
This guide provides step-by-step instructions to set up and run the backend task management API locally. The API provides secure, persistent task management with user isolation using JWT authentication.

## Prerequisites
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
Create a `.env` file in the backend-task-api directory with the following variables:

```env
# Database Configuration
DATABASE_URL="postgresql://username:password@localhost:5432/task_management"

# JWT Configuration
JWT_SECRET_KEY="your-super-secret-jwt-key-here"
JWT_ALGORITHM="HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
APP_ENV="development"
SERVER_HOST="0.0.0.0"
SERVER_PORT=8000
LOG_LEVEL="info"
```

For production, ensure you use strong, randomly generated secrets.

## Backend Setup (FastAPI)

### 1. Navigate to Backend Directory
```bash
cd backend-task-api  # From project root
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

## Running the API

### 1. Start the Service
Ensure the service is running at `http://localhost:8000`.

### 2. Access the API
The API endpoints are available at `http://localhost:8000/api/v1/`.

## API Endpoints

### Task Management Endpoints

#### GET /api/v1/tasks
Retrieve all tasks for the authenticated user.

**Headers**:
```
Authorization: Bearer <jwt_token_here>
```

**Query Parameters**:
- `completed` (optional): Filter by completion status (true/false)
- `limit` (optional): Number of tasks to return (default: 50, max: 100)
- `offset` (optional): Number of tasks to skip (for pagination)

#### POST /api/v1/tasks
Create a new task for the authenticated user.

**Headers**:
```
Authorization: Bearer <jwt_token_here>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "New task title",
  "description": "Optional task description",
  "completed": false
}
```

#### GET /api/v1/tasks/{task_id}
Retrieve a specific task.

**Headers**:
```
Authorization: Bearer <jwt_token_here>
```

#### PUT /api/v1/tasks/{task_id}
Update an existing task.

**Headers**:
```
Authorization: Bearer <jwt_token_here>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true
}
```

#### DELETE /api/v1/tasks/{task_id}
Delete a task.

**Headers**:
```
Authorization: Bearer <jwt_token_here>
```

#### PATCH /api/v1/tasks/{task_id}/toggle
Toggle the completion status of a task.

**Headers**:
```
Authorization: Bearer <jwt_token_here>
```

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

## Database Migrations

### Creating New Migrations
```bash
# From backend-task-api directory
alembic revision --autogenerate -m "Description of changes"
```

### Applying Migrations
```bash
# Apply all pending migrations
alembic upgrade head

# Downgrade to a specific version
alembic downgrade <revision-id>
```

## Testing the API

### 1. Unit Tests
Run backend unit tests:
```bash
cd backend-task-api
pytest tests/unit/
```

### 2. Integration Tests
Test the integration between components:
```bash
cd backend-task-api
pytest tests/integration/
```

### 3. Contract Tests
Test API contract compliance:
```bash
cd backend-task-api
pytest tests/contract/
```

## Production Deployment

### Building for Production
```bash
# Backend
cd backend-task-api
pip install -r requirements.txt
python -m compileall src/
```

### Environment Variables for Production
Ensure these variables are set in your production environment:
- `JWT_SECRET_KEY` (strong, randomly generated)
- `DATABASE_URL` (production database URL)
- `APP_ENV=production`
- `LOG_LEVEL=warning`