# Implementation Plan: Frontend & UX Integration

**Branch**: `001-frontend-ux-integration` | **Date**: 2026-01-09 | **Spec**: [link to spec](./spec.md)
**Input**: Feature specification from `/specs/001-frontend-ux-integration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Transform the single-user console todo app into a modern, secure, multi-user web application with authentication, responsive UI, and persistent storage using a fully spec-driven, no-manual-coding workflow. The implementation will follow an incremental approach focusing on authentication foundations, API integration, task management UI, and responsive layout.

## Technical Context

**Language/Version**: JavaScript/TypeScript, Next.js 16+ with React 19+
**Primary Dependencies**: 
- Next.js 16+ with App Router
- React 19+
- Better Auth with JWT plugin
- Tailwind CSS for styling
- Neon Serverless PostgreSQL (via backend API)
**Storage**: Browser local storage for JWT tokens, Neon Serverless PostgreSQL for task persistence
**Testing**: Jest, React Testing Library, Cypress for E2E testing
**Target Platform**: Web application supporting modern browsers on desktop and mobile
**Project Type**: Web application (Next.js frontend consuming backend API)
**Performance Goals**: Sub-200ms page load times, 95% uptime, support for 1000+ concurrent users
**Constraints**: <200ms p95 page load time, <100MB memory usage per client, mobile-responsive UI
**Scale/Scope**: Support for 10,000+ users, 1M+ tasks, horizontal scaling capability

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Constitution Compliance Verification:**
- [X] Correctness by Construction: All functionality defined in specs before implementation
- [X] Security-First Design: Authentication and authorization implemented from start
- [X] Clear Separation of Concerns: Frontend, backend, database, auth layers cleanly separated
- [X] Reproducibility: System buildable from specs, plans, and prompts
- [X] Maintainability: RESTful API conventions followed consistently
- [X] Quality Standards: API responses use consistent JSON structures

**Technology Stack Verification:**
- [X] Backend: Python FastAPI + SQLModel only (backend from Spec 2)
- [X] Frontend: Next.js 16+ App Router only
- [X] Database: Neon Serverless PostgreSQL only (via backend API)
- [X] Authentication: Better Auth with JWT plugin only
- [X] No manual coding (Claude Code only)

**Security Requirements Verification:**
- [X] Unauthorized requests return HTTP 401 (handled by backend)
- [X] Authenticated users can only read/write their own tasks (enforced by backend)
- [X] JWT signature verification required on backend (handled by auth library)
- [X] JWT expiration respected and enforced (handled by auth library)
- [X] User ID from JWT matches request context (enforced by backend)

## Project Structure

### Documentation (this feature)

```text
specs/001-frontend-ux-integration/
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
│   │           ├── page.tsx
│   │           └── [id]/
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

backend/  # From Spec 2 - consumed by frontend
├── src/
│   ├── models/
│   ├── services/
│   ├── api/
│   └── core/
├── alembic/
├── tests/
├── requirements.txt
└── pyproject.toml

docker-compose.yml
.env.example
README.md
```

**Structure Decision**: Web application with separate frontend and backend services following microservices architecture. The frontend consumes the backend API built in Spec 2 and implements authentication and task management UI. The architecture follows security-first principles with clear separation between frontend, backend, and database layers.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Separate services | Security isolation and scalability | Tight coupling would compromise security boundaries |
| JWT with custom verification | Better Auth doesn't directly integrate with FastAPI | Using session-based auth would complicate state management |

## Phase 0: Research & Unknown Resolution

### Research Tasks Completed

1. **Better Auth + Next.js App Router Integration**
   - Decision: Implement Better Auth with custom hooks for session management
   - Rationale: Better Auth provides seamless integration with Next.js App Router and handles JWT token management
   - Alternatives considered: Custom auth solution, other auth libraries

2. **API Client Best Practices for Next.js**
   - Decision: Create centralized API client that automatically attaches JWT tokens to all authenticated requests
   - Rationale: Ensures consistent authentication across all API calls and simplifies error handling
   - Alternatives considered: Per-component API calls, third-party HTTP libraries

3. **Responsive Design Patterns for Task Management**
   - Decision: Implement mobile-first responsive design using Tailwind CSS
   - Rationale: Provides consistent UX across devices with minimal code overhead
   - Alternatives considered: Separate mobile app, CSS-in-JS solutions

## Phase 1: Design & Contracts

### Data Model (data-model.md)

**User Entity** (from authentication system):
- id (string, primary key) - from JWT token
- email (string, unique)
- created_at (datetime)
- updated_at (datetime)

**Task Entity** (from backend API):
- id (string, primary key)
- title (string, not null)
- description (text, optional)
- completed (boolean, default: false)
- user_id (string, foreign key to User)
- created_at (datetime)
- updated_at (datetime)

### API Contracts (contracts/)

**Authentication Endpoints** (consumed from backend API):
- POST /api/v1/auth/login - Authenticate user and return JWT
- POST /api/v1/auth/register - Register new user and return JWT
- POST /api/v1/auth/logout - Invalidate session

**Task Endpoints** (consumed from backend API):
- GET /api/v1/tasks - Retrieve user's tasks
- POST /api/v1/tasks - Create new task
- GET /api/v1/tasks/{task_id} - Retrieve specific task
- PUT /api/v1/tasks/{task_id} - Update task
- DELETE /api/v1/tasks/{task_id} - Delete task
- PATCH /api/v1/tasks/{task_id}/toggle - Toggle completion status

### Quickstart Guide (quickstart.md)

1. Clone the repository
2. Set up environment variables (backend API URL, auth config)
3. Install frontend dependencies: `cd frontend && npm install`
4. Start the frontend development server: `cd frontend && npm run dev`
5. Ensure backend API from Spec 2 is running
6. Access the application at http://localhost:3000

### Agent Context Update

The agent context has been updated with the following technologies:
- Next.js 16+ with App Router
- Better Auth with JWT plugin
- Tailwind CSS for responsive design
- Neon Serverless PostgreSQL (via backend API)
- JWT-based authentication patterns