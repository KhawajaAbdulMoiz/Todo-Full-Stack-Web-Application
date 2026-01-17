# Implementation Plan: Multi-User Todo Web Application

**Branch**: `001-multi-user-todo` | **Date**: 2026-01-09 | **Spec**: [link to spec](./spec.md)
**Input**: Feature specification from `/specs/001-multi-user-todo/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Transform a single-user console todo app into a modern, secure, multi-user web application using a fully spec-driven, no-manual-coding workflow. The implementation will follow an incremental approach focusing on authentication foundations, backend API with database integration, and frontend integration. The system will use JWT-based authentication for secure user isolation and Neon Serverless PostgreSQL for persistent data storage.

## Technical Context

**Language/Version**: Python 3.11 (backend), JavaScript/TypeScript (frontend), Node.js 18+
**Primary Dependencies**:
- Backend: FastAPI, SQLModel, Pydantic, uvicorn
- Frontend: Next.js 16+, React 19+, Better Auth, Tailwind CSS
- Database: Neon Serverless PostgreSQL, asyncpg
**Storage**: Neon Serverless PostgreSQL database with SQLModel ORM
**Testing**: pytest (backend), Jest/React Testing Library (frontend), Supertest for API testing
**Target Platform**: Web application supporting modern browsers on desktop and mobile
**Project Type**: Web application (separate frontend and backend)
**Performance Goals**: Sub-200ms API response times, 95% uptime, support for 1000+ concurrent users
**Constraints**: <200ms p95 API response time, <100MB memory usage per service, mobile-responsive UI
**Scale/Scope**: Support for 10,000+ users, 1M+ tasks, horizontal scaling capability

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Constitution Compliance Verification:**
- [x] Correctness by Construction: All functionality defined in specs before implementation
- [x] Security-First Design: Authentication and authorization implemented from start
- [x] Clear Separation of Concerns: Frontend, backend, database, auth layers cleanly separated
- [x] Reproducibility: System buildable from specs, plans, and prompts
- [x] Maintainability: RESTful API conventions followed consistently
- [x] Quality Standards: API responses use consistent JSON structures

**Technology Stack Verification:**
- [x] Backend: Python FastAPI + SQLModel only
- [x] Frontend: Next.js 16+ App Router only
- [x] Database: Neon Serverless PostgreSQL only
- [x] Authentication: Better Auth with JWT plugin only
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
specs/001-multi-user-todo/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application structure
backend/
├── src/
│   ├── models/
│   │   ├── user.py
│   │   └── task.py
│   ├── services/
│   │   ├── auth_service.py
│   │   └── task_service.py
│   ├── api/
│   │   ├── deps.py
│   │   ├── auth.py
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

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── auth/
│   │   │   ├── login/
│   │   │   ├── register/
│   │   │   └── middleware.ts
│   │   └── dashboard/
│   │       ├── page.tsx
│   │       └── tasks/
│   ├── components/
│   │   ├── ui/
│   │   ├── auth/
│   │   └── tasks/
│   ├── lib/
│   │   ├── auth.ts
│   │   ├── api.ts
│   │   └── types.ts
│   └── styles/
├── public/
├── package.json
├── tailwind.config.js
└── next.config.js

docker-compose.yml
.env.example
README.md
```

**Structure Decision**: Web application with separate backend and frontend services following microservices architecture. The backend provides a REST API using FastAPI, while the frontend is a Next.js application that consumes the API. Database layer is handled by SQLModel with Neon Serverless PostgreSQL.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Separate services | Security isolation and scalability | Tight coupling would compromise security boundaries |
| JWT with custom verification | Better Auth doesn't directly integrate with FastAPI | Using session-based auth would complicate state management |

## Phase 0: Research & Unknown Resolution

### Research Tasks Completed

1. **Better Auth + FastAPI Integration**
   - Decision: Implement custom JWT verification middleware in FastAPI to work with Better Auth
   - Rationale: Better Auth handles frontend authentication and token issuance, while FastAPI implements custom verification
   - Alternatives considered: Session-based auth, custom auth solution

2. **SQLModel Best Practices for Neon PostgreSQL**
   - Decision: Use async SQLAlchemy engine with asyncpg driver for optimal Neon performance
   - Rationale: Neon's serverless nature benefits from async operations and connection pooling
   - Alternatives considered: Traditional sync connections, other ORMs

3. **Next.js 16+ App Router Patterns**
   - Decision: Implement protected routes using middleware and client-side auth state management
   - Rationale: App Router provides better performance and developer experience
   - Alternatives considered: Pages router, custom routing solution

## Phase 1: Design & Contracts

### Data Model (data-model.md)

**User Entity**:
- id (UUID, primary key)
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

**Authentication Endpoints**:
- POST /api/auth/register - Register new user
- POST /api/auth/login - Authenticate user and return JWT
- POST /api/auth/logout - Invalidate session

**Task Endpoints**:
- GET /api/tasks - Retrieve user's tasks
- POST /api/tasks - Create new task
- PUT /api/tasks/{task_id} - Update task
- DELETE /api/tasks/{task_id} - Delete task
- PATCH /api/tasks/{task_id}/toggle - Toggle completion status

### Quickstart Guide (quickstart.md)

1. Clone the repository
2. Set up environment variables (database URL, auth secret)
3. Install backend dependencies: `cd backend && pip install -r requirements.txt`
4. Install frontend dependencies: `cd frontend && npm install`
5. Run database migrations: `cd backend && alembic upgrade head`
6. Start backend: `cd backend && uvicorn src.main:app --reload`
7. Start frontend: `cd frontend && npm run dev`
8. Access the application at http://localhost:3000

### Agent Context Update

The agent context has been updated with the following technologies:
- Next.js 16+ with App Router
- Python FastAPI with SQLModel
- Better Auth with JWT
- Neon Serverless PostgreSQL
- Async SQLAlchemy patterns
