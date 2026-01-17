# Authentication System Implementation

## Overview
The authentication system for the Todo application implements secure user registration, login, and logout functionality using JWT tokens and bcrypt password hashing.

## Features Implemented

### 1. User Registration (`POST /auth/register`)
- Accepts email and password via form data
- Hashes passwords using bcrypt
- Creates new user record in the database
- Generates JWT access token upon successful registration
- Returns token, token type, and user information
- Prevents duplicate email registrations

### 2. User Login (`POST /auth/login`)
- Accepts email and password via form data
- Verifies credentials against stored password hash
- Generates JWT access token upon successful authentication
- Returns token, token type, and user information
- Returns 401 error for invalid credentials

### 3. User Logout (`POST /auth/logout`)
- Accepts JWT token via Authorization header
- Adds token to blacklist to prevent reuse
- Implements token invalidation
- Returns success message

## Security Features

### Password Security
- Passwords are hashed using bcrypt with automatic salt generation
- Passwords are never stored in plain text
- Uses Passlib's CryptContext for secure password handling

### Token Security
- JWT tokens with configurable expiration (30 minutes)
- Tokens contain user ID and email for identification
- Secret key stored in environment variables
- Blacklist mechanism to invalidate tokens before expiration

### Token Blacklisting
- Maintains a database of invalidated tokens
- Checks for blacklisted tokens during authentication
- Automatic cleanup of expired tokens
- Prevents use of logged-out tokens

## Models Used

### User Model
- Stores user information (email, password hash)
- UUID primary key for security
- Created/updated timestamps

### Token Blacklist Model
- Tracks invalidated JWT tokens
- Includes expiration timestamp
- Enables cleanup of expired entries

## Dependencies
- FastAPI for web framework
- SQLModel for database modeling
- Passlib with bcrypt for password hashing
- python-jose for JWT handling
- asyncpg for PostgreSQL async operations

## Error Handling
- Proper HTTP status codes (201 for registration, 401 for unauthorized, 409 for conflicts)
- Detailed error messages
- Secure error responses that don't expose sensitive information

## API Response Format
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
}
```

## Environment Variables Required
- `BETTER_AUTH_SECRET`: Secret key for JWT signing
- `DATABASE_URL`: Database connection string

## Testing
Unit tests are included to verify:
- Successful user registration
- Successful user login
- Proper logout functionality
- Token invalidation after logout