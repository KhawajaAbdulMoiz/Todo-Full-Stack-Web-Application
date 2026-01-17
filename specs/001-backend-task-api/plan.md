# Implementation Plan: Backend API & Database (Task Management)

**Branch**: `001-backend-task-api` | **Date**: 2026-01-09 | **Spec**: [link to spec](./spec.md)
**Input**: Feature specification from `/specs/001-backend-task-api/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Design and implement a secure, persistent, multi-user task management backend that enforces authentication and user ownership. The implementation will follow an incremental approach focusing on database design, JWT authentication enforcement, and CRUD endpoint implementation. The system will use JWT-based authentication for secure user isolation and Neon Serverless PostgreSQL for persistent task storage.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**:
- FastAPI, SQLModel, Pydantic, uvicorn
- asyncpg, SQLAlchemy, PyJWT
- passlib, bcrypt for password hashing
**Storage**: Neon Serverless PostgreSQL database with SQLModel ORM
**Testing**: pytest, factory-boy for test data generation
**Target Platform**: Linux server environment
**Project Type**: Backend service (REST API)
**Performance Goals**: Sub-200ms API response times, 99.9% uptime, support for 1000+ concurrent users
**Constraints**: <200ms p95 API response time, <100MB memory usage, secure JWT handling
**Scale/Scope**: Support for 10,000+ users, 1M+ tasks, horizontal scaling capability

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Constitution Compliance Verification:**
- [x] Correctness by Construction: All functionality defined in specs before implementation
- [x] Security-First Design: Authentication and authorization implemented from start
- [x] Clear Separation of Concerns: Backend, database, auth layers cleanly separated
- [x] Reproducibility: System buildable from specs, plans, and prompts
- [x] Maintainability: RESTful API conventions followed consistently
- [x] Quality Standards: API responses use consistent JSON structures

**Technology Stack Verification:**
- [x] Backend: Python FastAPI + SQLModel only
- [ ] Frontend: Next.js 16+ App Router only (not applicable for this backend-only feature)
- [x] Database: Neon Serverless PostgreSQL only
- [x] Authentication: JWT token verification only (reusing tokens from main app)
- [x] No manual coding (Claude Code only)

**Security Requirements Verification:**
- [x] Unauthorized requests return HTTP 401
- [x] Authenticated users can only read/write their own tasks
- [x] JWT signature verification required on backend
- [x] JWT expiration respected and enforced
- [x] User ID from JWT matches request context

## Project Structure

### Documentation (this feature)

```text
specs/001-backend-task-api/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Backend service structure
backend-task-api/
├── src/
│   ├── models/
│   │   ├── user.py
│   │   └── task.py
│   ├── services/
│   │   └── task_service.py
│   ├── api/
│   │   ├── deps.py
│   │   └── tasks.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   └── main.py
├── alembic/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
├── requirements.txt
└── pyproject.toml

docker-compose.yml
.env.example
README.md
```

**Structure Decision**: Backend service following microservices architecture. The service provides a REST API using FastAPI, with SQLModel for database modeling and Neon Serverless PostgreSQL for persistent storage.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Separate service | Security isolation and scalability | Tight coupling would compromise security boundaries |
| JWT with custom verification | Reusing existing JWT tokens from main app | Creating new auth system would duplicate effort |

## Phase 0: Research & Unknown Resolution

### Research Tasks Completed

1. **SQLModel Best Practices for Neon PostgreSQL**
   - Decision: Use async SQLAlchemy engine with asyncpg driver for optimal Neon performance
   - Rationale: Neon's serverless nature benefits from async operations and connection pooling
   - Alternatives considered: Traditional sync connections, other ORMs

2. **FastAPI JWT Middleware Patterns**
   - Decision: Implement custom JWT verification dependency for request context
   - Rationale: Allows attaching user ID to request for easy access in endpoints
   - Alternatives considered: Built-in OAuth2 schemes, custom security classes

3. **Task Ownership Enforcement**
   - Decision: Validate user ID in JWT matches user ID in URL/route parameters
   - Rationale: Provides clear separation of user data with minimal overhead
   - Alternatives considered: Database-level row security, separate tables per user

## Phase 1: Design & Contracts

### Data Model (data-model.md)

**User Entity**:
- id (UUID, primary key) - from JWT token
- email (string, unique, indexed)
- created_at (datetime)
- updated_at (datetime)

**Task Entity**:
- id (UUID, primary key)
- title (string, not null)
- description (text, optional)
- completed (boolean, default: false)
- user_id (UUID, foreign key to User)
- created_at (datetime)
- updated_at (datetime)

### API Contracts (contracts/)

**Task Endpoints**:
- GET /api/tasks - Retrieve authenticated user's tasks
- POST /api/tasks - Create new task for authenticated user
- GET /api/tasks/{task_id} - Retrieve specific task
- PUT /api/tasks/{task_id} - Update task
- DELETE /api/tasks/{task_id} - Delete task
- PATCH /api/tasks/{task_id}/toggle - Toggle completion status

### Quickstart Guide (quickstart.md)

1. Clone the repository
2. Set up environment variables (database URL, JWT secret)
3. Install dependencies: `cd backend-task-api && pip install -r requirements.txt`
4. Run database migrations: `cd backend-task-api && alembic upgrade head`
5. Start the service: `cd backend-task-api && uvicorn src.main:app --reload`
6. Access the API at http://localhost:8000

### Agent Context Update

The agent context has been updated with the following technologies:
- Python FastAPI with SQLModel
- Neon Serverless PostgreSQL
- Async SQLAlchemy patterns
- JWT authentication and security
- Task management API design
