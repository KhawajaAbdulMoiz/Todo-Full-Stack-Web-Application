# Data Model: Multi-User Todo Web Application

## Overview
This document defines the data entities and relationships for the multi-user todo web application. The model follows normalization principles and includes proper validation and indexing for optimal performance.

## Entity: User

### Fields
- **id** (UUID, Primary Key)
  - Type: UUID (Universally Unique Identifier)
  - Constraints: Not null, Unique, Auto-generated
  - Purpose: Unique identifier for each user
  
- **email** (String)
  - Type: String (Email format)
  - Constraints: Not null, Unique, Indexed, Max length 255
  - Purpose: User's email address for authentication and identification
  
- **password_hash** (String)
  - Type: String (Hashed)
  - Constraints: Not null, Max length 255
  - Purpose: Securely stored hashed password (never store plain text passwords)
  
- **created_at** (DateTime)
  - Type: DateTime (UTC)
  - Constraints: Not null, Auto-generated
  - Purpose: Timestamp of user account creation
  
- **updated_at** (DateTime)
  - Type: DateTime (UTC)
  - Constraints: Not null, Auto-generated, Updated on change
  - Purpose: Timestamp of last user record update

### Relationships
- One-to-Many: User → Tasks (one user can have many tasks)

### Validation Rules
- Email must be a valid email format
- Password must meet minimum strength requirements (handled by Better Auth)
- Email uniqueness is enforced at the database level

### Indexes
- Primary index on `id`
- Unique index on `email`
- Index on `created_at` for sorting/filtering

## Entity: Task

### Fields
- **id** (UUID, Primary Key)
  - Type: UUID (Universally Unique Identifier)
  - Constraints: Not null, Unique, Auto-generated
  - Purpose: Unique identifier for each task
  
- **title** (String)
  - Type: String
  - Constraints: Not null, Max length 255
  - Purpose: Brief title or description of the task
  
- **description** (Text)
  - Type: Text (Optional)
  - Constraints: Nullable, Max length 1000
  - Purpose: Detailed description of the task (optional)
  
- **completed** (Boolean)
  - Type: Boolean
  - Constraints: Not null, Default false
  - Purpose: Indicates whether the task is completed
  
- **user_id** (UUID, Foreign Key)
  - Type: UUID
  - Constraints: Not null, References User.id
  - Purpose: Links the task to the user who owns it
  
- **created_at** (DateTime)
  - Type: DateTime (UTC)
  - Constraints: Not null, Auto-generated
  - Purpose: Timestamp of task creation
  
- **updated_at** (DateTime)
  - Type: DateTime (UTC)
  - Constraints: Not null, Auto-generated, Updated on change
  - Purpose: Timestamp of last task update

### Relationships
- Many-to-One: Task → User (many tasks belong to one user)

### Validation Rules
- Title must not be empty
- User_id must reference an existing user
- Completed status can only be true/false

### Indexes
- Primary index on `id`
- Index on `user_id` for efficient user-based queries
- Index on `completed` for filtering completed/incomplete tasks
- Composite index on `user_id` and `completed` for efficient user task filtering
- Index on `created_at` for chronological ordering

## Entity Relationship Diagram

```
┌─────────────────────────┐         ┌─────────────────────────┐
│         User            │         │          Task           │
├─────────────────────────┤    ┌───▶├─────────────────────────┤
│ id: UUID (PK)           │    │    │ id: UUID (PK)           │
│ email: String (unique)  │    │    │ title: String           │
│ password_hash: String   │    │    │ description: Text       │
│ created_at: DateTime    │    │    │ completed: Boolean      │
│ updated_at: DateTime    │    │    │ user_id: UUID (FK)      │
└─────────────────────────┘    │    │ created_at: DateTime    │
                               │    │ updated_at: DateTime    │
                               └────┴─────────────────────────┘
```

## Business Rules

1. **User Isolation**: Each task belongs exclusively to one user, and users can only access their own tasks
2. **Data Integrity**: Foreign key constraints ensure that tasks always reference valid users
3. **Immutability**: User and task IDs are immutable once created
4. **Audit Trail**: Created and updated timestamps provide audit trail for all records
5. **Soft Deletes**: Instead of deleting records, consider adding a `deleted_at` field to maintain data integrity

## State Transitions

### Task State Transitions
- **Incomplete** → **Complete**: When user marks task as done
- **Complete** → **Incomplete**: When user unmarks task as done

### Transition Validation
- Only the owner of a task can change its completion status
- Task completion status can only transition between true/false values

## API Representation

### User Object (JSON)
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "created_at": "2026-01-09T10:00:00Z",
  "updated_at": "2026-01-09T10:00:00Z"
}
```

### Task Object (JSON)
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "title": "Complete project specification",
  "description": "Finish writing the detailed specification for the todo app",
  "completed": false,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2026-01-09T10:00:00Z",
  "updated_at": "2026-01-09T10:00:00Z"
}
```