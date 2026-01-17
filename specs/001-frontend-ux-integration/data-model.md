# Data Model: Frontend & UX Integration

## Overview
This document defines the frontend data models and representations for the multi-user todo application. The frontend consumes data models from the backend API but may have additional client-side representations for UI state and user experience.

## Entity: User (Client Representation)

### Fields
- **id** (String)
  - Type: String (UUID format)
  - Source: Extracted from JWT token
  - Constraints: Not null, Unique, Immutable
  - Purpose: Unique identifier for each user

- **email** (String)
  - Type: String (Email format)
  - Source: Authentication system
  - Constraints: Not null, Unique, Indexed, Max length 255
  - Purpose: User's email address for identification

- **isLoggedIn** (Boolean)
  - Type: Boolean
  - Source: Authentication state
  - Constraints: Not null, Default false
  - Purpose: Indicates if user is currently authenticated

- **sessionExpiresAt** (DateTime)
  - Type: DateTime (ISO 8601 format)
  - Source: JWT token expiration claim
  - Constraints: Nullable
  - Purpose: Timestamp when current session expires

### Relationships
- One-to-Many: User → Tasks (one user can have many tasks)

### Validation Rules
- Email must be a valid email format
- Session expiration must be in the future when valid

### Indexes
- Primary index on `id`
- Index on `email` for efficient lookup
- Index on `sessionExpiresAt` for session management

## Entity: Task (Client Representation)

### Fields
- **id** (String)
  - Type: String (UUID format)
  - Source: Backend API
  - Constraints: Not null, Unique, Immutable
  - Purpose: Unique identifier for each task

- **title** (String)
  - Type: String
  - Source: Backend API
  - Constraints: Not null, Max length 255
  - Purpose: Brief title or description of the task

- **description** (Text)
  - Type: Text (Optional)
  - Source: Backend API
  - Constraints: Nullable, Max length 1000
  - Purpose: Detailed description of the task (optional)

- **completed** (Boolean)
  - Type: Boolean
  - Source: Backend API
  - Constraints: Not null, Default false
  - Purpose: Indicates whether the task is completed

- **userId** (String)
  - Type: String (UUID format)
  - Source: Backend API
  - Constraints: Not null, References User.id
  - Purpose: Links the task to the user who owns it

- **createdAt** (DateTime)
  - Type: DateTime (ISO 8601 format)
  - Source: Backend API
  - Constraints: Not null
  - Purpose: Timestamp of task creation

- **updatedAt** (DateTime)
  - Type: DateTime (ISO 8601 format)
  - Source: Backend API
  - Constraints: Not null
  - Purpose: Timestamp of last task update

- **isLoading** (Boolean)
  - Type: Boolean
  - Source: Client state
  - Constraints: Not null, Default false
  - Purpose: Indicates if task is currently being updated

### Relationships
- Many-to-One: Task → User (many tasks belong to one user)

### Validation Rules
- Title must not be empty
- User_id must reference an existing user
- Completed status can only be true/false values

### Indexes
- Primary index on `id`
- Index on `userId` for efficient user-based queries
- Index on `completed` for filtering completed/incomplete tasks
- Composite index on `userId` and `completed` for efficient user task filtering
- Index on `createdAt` for chronological ordering

## Entity: API Response Wrapper

### Fields
- **success** (Boolean)
  - Type: Boolean
  - Source: API response
  - Constraints: Not null
  - Purpose: Indicates if the API request was successful

- **data** (Any)
  - Type: Any (depends on endpoint)
  - Source: API response
  - Constraints: Nullable
  - Purpose: Contains the requested data

- **message** (String)
  - Type: String
  - Source: API response
  - Constraints: Nullable
  - Purpose: Optional success message

- **error** (Object)
  - Type: Object
  - Source: API response
  - Constraints: Nullable
  - Purpose: Contains error details when success is false

### Error Object Fields
- **code** (String): Error code from the backend
- **message** (String): Human-readable error message
- **details** (Object): Additional error details (optional)

## Entity: UI State

### Fields
- **isLoading** (Boolean)
  - Type: Boolean
  - Source: Client state
  - Constraints: Not null, Default false
  - Purpose: Indicates if data is being loaded

- **hasError** (Boolean)
  - Type: Boolean
  - Source: Client state
  - Constraints: Not null, Default false
  - Purpose: Indicates if an error occurred

- **errorMessage** (String)
  - Type: String
  - Source: Client state
  - Constraints: Nullable
  - Purpose: Contains error message when hasError is true

- **isAuthenticated** (Boolean)
  - Type: Boolean
  - Source: Authentication state
  - Constraints: Not null, Default false
  - Purpose: Indicates if user is authenticated

## Business Rules (Client-Side)

1. **User Isolation**: UI only displays tasks belonging to the authenticated user
2. **Session Management**: UI automatically redirects to login when session expires
3. **Offline Handling**: UI provides appropriate feedback when API is unreachable
4. **Loading States**: UI shows loading indicators during API operations
5. **Error Handling**: UI displays user-friendly error messages for failed operations

## State Transitions

### Task State Transitions
- **Incomplete** → **Complete**: When user toggles completion status
- **Complete** → **Incomplete**: When user untoggles completion status

### Transition Validation
- Only authenticated users can change task completion status
- Task completion status can only transition between true/false values

### User Authentication Transitions
- **Logged Out** → **Logging In** → **Logged In**: During login process
- **Logged In** → **Session Expired** → **Logged Out**: When JWT expires

## API Representation

### User Object (JSON)
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "isLoggedIn": true,
  "sessionExpiresAt": "2026-01-09T11:00:00Z"
}
```

### Task Object (JSON)
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "title": "Complete project specification",
  "description": "Finish writing the detailed specification for the todo app",
  "completed": false,
  "userId": "550e8400-e29b-41d4-a716-446655440000",
  "createdAt": "2026-01-09T10:00:00Z",
  "updatedAt": "2026-01-09T10:00:00Z",
  "isLoading": false
}
```

### API Response Wrapper (JSON)
```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Optional success message",
  "error": { /* error details when success is false */ }
}
```

### Error Response (JSON)
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