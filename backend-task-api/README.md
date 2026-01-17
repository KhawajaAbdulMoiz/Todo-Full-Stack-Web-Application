# Backend Task API

This is the backend service for the task management application. It provides a secure, persistent, multi-user task management API that enforces authentication and user ownership.

## Features

- Secure JWT-based authentication
- User isolation (users can only access their own tasks)
- Full CRUD operations for tasks
- RESTful API design
- Neon Serverless PostgreSQL database

## Tech Stack

- Python 3.11
- FastAPI
- SQLModel
- Neon Serverless PostgreSQL
- JWT for authentication

## Setup

1. Clone the repository
2. Navigate to the `backend-task-api` directory
3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up environment variables by copying `.env.example` to `.env` and filling in the values
6. Run database migrations:
   ```bash
   alembic upgrade head
   ```
7. Start the server:
   ```bash
   uvicorn src.main:app --reload
   ```

## API Endpoints

### Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token_here>
```

### Task Management Endpoints

#### GET /api/v1/tasks
Retrieve all tasks for the authenticated user.

#### POST /api/v1/tasks
Create a new task for the authenticated user.

#### GET /api/v1/tasks/{task_id}
Retrieve a specific task.

#### PUT /api/v1/tasks/{task_id}
Update an existing task.

#### DELETE /api/v1/tasks/{task_id}
Delete a task.

#### PATCH /api/v1/tasks/{task_id}/toggle
Toggle the completion status of a task.

## Environment Variables

- `DATABASE_URL`: Database connection string
- `JWT_SECRET_KEY`: Secret key for JWT signing
- `JWT_ALGORITHM`: Algorithm for JWT signing (default: HS256)
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: Expiration time for JWT tokens (default: 30)
- `APP_ENV`: Application environment (default: development)
- `SERVER_HOST`: Host for the server (default: 0.0.0.0)
- `SERVER_PORT`: Port for the server (default: 8000)
- `LOG_LEVEL`: Log level (default: info)

## Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src
```

## License

This project is licensed under the MIT License.