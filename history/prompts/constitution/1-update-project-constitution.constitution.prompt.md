---
id: 1
title: "Update Project Constitution"
stage: constitution
date_iso: "2026-01-09"
surface: "agent"
model: "claude-sonnet-4"
feature: "none"
branch: "main"
command: "/sp.constitution"
labels: ["constitution", "governance", "specification"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".specify/memory/constitution.md"
  - ".specify/templates/plan-template.md"
  - ".specify/templates/spec-template.md"
  - ".specify/templates/tasks-template.md"
tests: []
---

# Prompt History Record: Update Project Constitution

## Original Prompt

```
Project: Multi-user Todo Full-Stack Web Application (Spec-Driven, Agentic Dev Stack)

Core principles:
- Correctness by construction (spec-first, no manual coding)
- Security-first design (authentication, authorization, user isolation)
- Clear separation of concerns (frontend, backend, database, auth)
- Reproducibility (entire system buildable from specs, plans, and prompts)
- Maintainability (clean APIs, consistent schemas, predictable behavior)

Key standards:
- All functionality must be explicitly defined in specs before implementation
- All API endpoints must enforce authentication and user ownership
- JWT-based authentication must be verified on every backend request
- No hardcoded secrets; all secrets via environment variables
- RESTful API conventions must be followed consistently
- Database schema changes must be traceable and version-safe
- Frontend must not access data outside authenticated user context

Constraints:
- No manual coding allowed (Claude Code only)
- Backend: Python FastAPI + SQLModel only
- Frontend: Next.js 16+ App Router only
- Database: Neon Serverless PostgreSQL only
- Authentication: Better Auth with JWT plugin only
- Auth secret must be shared via BETTER_AUTH_SECRET environment variable
- All endpoints require valid JWT after authentication is enabled
- System must support multiple concurrent users

Security requirements:
- Unauthorized requests return HTTP 401
- Authenticated users can only read/write their own tasks
- JWT signature verification required on backend
- JWT expiration respected and enforced
- User ID from JWT must match request context

Quality standards:
- API responses must use consistent JSON structures
- Errors must return meaningful HTTP status codes
- Frontend must be responsive and mobile-friendly
- Code generated must be readable and logically structured
- No unused endpoints, models, or components

Success criteria:
- Users can sign up and sign in successfully
- JWT tokens are issued, transmitted, and verified correctly
- Users can only see and modify their own tasks
- All CRUD task operations work end-to-end
- Database persists data across sessions
- Entire application can be rebuilt from specs and plans alone
- Passes hackathon review for correctness, security, and architecture
```

## Response Summary

Updated the project constitution file (.specify/memory/constitution.md) to reflect the Multi-user Todo Full-Stack Web Application requirements, including all core principles, technology stack requirements, security requirements, and quality standards. Also updated the related templates (plan, spec, tasks) to align with the new constitution and ensure consistency across the project.

## Outcome

Successfully created a comprehensive constitution document that establishes governance for the Multi-user Todo Full-Stack Web Application project. The constitution enforces security-first design, clear separation of concerns, and spec-driven development practices. Related templates were updated to ensure consistency and compliance with the new governance structure.

## Evaluation

The constitution update successfully captures all specified requirements and principles. The version was incremented from 1.0.0 to 1.1.0 to reflect the addition of new principles and requirements. Template files were updated to include constitution compliance checks and verification steps to ensure ongoing adherence to the established principles.