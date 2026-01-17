# API Contracts: Frontend & UX Integration

## Overview
This document defines the API contracts that the frontend consumes from the backend API built in Spec 2. All endpoints require JWT authentication in the Authorization header, except for authentication endpoints.

## Base URL
```
https://api.taskflow.com/v1    # Production
http://localhost:8000/api/v1   # Development
```

## Authentication
All endpoints (except authentication endpoints) require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token_here>
```

## Common Response Format

### Success Response
```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Optional success message"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": { /* optional error details */ }
  }
}
```

## Authentication Endpoints

### POST /auth/register
Register a new user account.

#### Request
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

#### Response (201 Created)
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "user@example.com",
      "createdAt": "2026-01-09T10:00:00Z",
      "updatedAt": "2026-01-09T10:00:00Z"
    },
    "token": "jwt_token_here"
  },
  "message": "Registration successful"
}
```

#### Error Responses
- `400 Bad Request`: Invalid input data
- `409 Conflict`: User with email already exists

---

### POST /auth/login
Authenticate user and return JWT token.

#### Request
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

#### Response (200 OK)
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "user@example.com",
      "createdAt": "2026-01-09T10:00:00Z",
      "updatedAt": "2026-01-09T10:00:00Z"
    },
    "token": "jwt_token_here"
  },
  "message": "Login successful"
}
```

#### Error Responses
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid credentials

---

### POST /auth/logout
Invalidate user session (server-side logout).

#### Headers
```
Authorization: Bearer <jwt_token_here>
```

#### Response (200 OK)
```json
{
  "success": true,
  "message": "Logout successful"
}
```

#### Error Responses
- `401 Unauthorized`: Invalid or expired token

---

## Task Management Endpoints

### GET /tasks
Retrieve all tasks for the authenticated user.

#### Headers
```
Authorization: Bearer <jwt_token_here>
```

#### Query Parameters
- `completed` (optional): Filter by completion status (true/false)
- `limit` (optional): Number of tasks to return (default: 50, max: 100)
- `offset` (optional): Number of tasks to skip (for pagination)

#### Response (200 OK)
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "title": "Complete project specification",
        "description": "Finish writing the detailed specification for the todo app",
        "completed": false,
        "userId": "550e8400-e29b-41d4-a716-446655440000",
        "createdAt": "2026-01-09T10:00:00Z",
        "updatedAt": "2026-01-09T10:00:00Z"
      }
    ],
    "pagination": {
      "total": 1,
      "limit": 50,
      "offset": 0
    }
  }
}
```

#### Error Responses
- `401 Unauthorized`: Invalid or expired token

---

### POST /tasks
Create a new task for the authenticated user.

#### Headers
```
Authorization: Bearer <jwt_token_here>
Content-Type: application/json
```

#### Request
```json
{
  "title": "New task title",
  "description": "Optional task description",
  "completed": false
}
```

#### Response (201 Created)
```json
{
  "success": true,
  "data": {
    "task": {
      "id": "550e8400-e29b-41d4-a716-446655440002",
      "title": "New task title",
      "description": "Optional task description",
      "completed": false,
      "userId": "550e8400-e29b-41d4-a716-446655440000",
      "createdAt": "2026-01-09T10:00:00Z",
      "updatedAt": "2026-01-09T10:00:00Z"
    }
  },
  "message": "Task created successfully"
}
```

#### Error Responses
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid or expired token

---

### GET /tasks/{task_id}
Retrieve a specific task.

#### Path Parameters
- `task_id`: UUID of the task to retrieve

#### Headers
```
Authorization: Bearer <jwt_token_here>
```

#### Response (200 OK)
```json
{
  "success": true,
  "data": {
    "task": {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "title": "Complete project specification",
      "description": "Finish writing the detailed specification for the todo app",
      "completed": false,
      "userId": "550e8400-e29b-41d4-a716-446655440000",
      "createdAt": "2026-01-09T10:00:00Z",
      "updatedAt": "2026-01-09T10:00:00Z"
    }
  }
}
```

#### Error Responses
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: User does not own the task
- `404 Not Found`: Task does not exist

---

### PUT /tasks/{task_id}
Update an existing task.

#### Path Parameters
- `task_id`: UUID of the task to update

#### Headers
```
Authorization: Bearer <jwt_token_here>
Content-Type: application/json
```

#### Request
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true
}
```

#### Response (200 OK)
```json
{
  "success": true,
  "data": {
    "task": {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "title": "Updated task title",
      "description": "Updated task description",
      "completed": true,
      "userId": "550e8400-e29b-41d4-a716-446655440000",
      "createdAt": "2026-01-09T10:00:00Z",
      "updatedAt": "2026-01-09T11:00:00Z"
    }
  },
  "message": "Task updated successfully"
}
```

#### Error Responses
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: User does not own the task
- `404 Not Found`: Task does not exist

---

### DELETE /tasks/{task_id}
Delete a task.

#### Path Parameters
- `task_id`: UUID of the task to delete

#### Headers
```
Authorization: Bearer <jwt_token_here>
```

#### Response (200 OK)
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

#### Error Responses
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: User does not own the task
- `404 Not Found`: Task does not exist

---

### PATCH /tasks/{task_id}/toggle-completion
Toggle the completion status of a task.

#### Path Parameters
- `task_id`: UUID of the task to toggle

#### Headers
```
Authorization: Bearer <jwt_token_here>
```

#### Response (200 OK)
```json
{
  "success": true,
  "data": {
    "task": {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "title": "Complete project specification",
      "description": "Finish writing the detailed specification for the todo app",
      "completed": true,
      "userId": "550e8400-e29b-41d4-a716-446655440000",
      "createdAt": "2026-01-09T10:00:00Z",
      "updatedAt": "2026-01-09T12:00:00Z"
    }
  },
  "message": "Task completion status toggled"
}
```

#### Error Responses
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: User does not own the task
- `404 Not Found`: Task does not exist

## Error Codes

| Code | Description |
|------|-------------|
| AUTH_001 | Invalid credentials |
| AUTH_002 | Token expired |
| AUTH_003 | Invalid token |
| AUTH_004 | Insufficient permissions |
| VALIDATION_001 | Invalid input format |
| VALIDATION_002 | Missing required field |
| RESOURCE_001 | Resource not found |
| RESOURCE_002 | Resource already exists |
| SERVER_001 | Internal server error |