<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Modified principles: None (new principles added)
Added sections: Core Principles (6 principles), Additional Constraints, Security Requirements, Quality Standards, Success Criteria
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ⚠ pending
Runtime docs requiring updates: README.md ⚠ pending
Follow-up TODOs: None
-->

# Multi-user Todo Full-Stack Web Application Constitution

## Core Principles

### I. Correctness by Construction
Spec-first approach: All functionality must be explicitly defined in specs before implementation; No manual coding allowed (Claude Code only); Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code.

### II. Security-First Design
Authentication and authorization must be implemented from the start; All API endpoints must enforce authentication and user ownership; JWT-based authentication must be verified on every backend request; Auth secret must be shared via BETTER_AUTH_SECRET environment variable.

### III. Clear Separation of Concerns
Frontend, backend, database, and authentication layers must be cleanly separated; Backend: Python FastAPI + SQLModel only; Frontend: Next.js 16+ App Router only; Database: Neon Serverless PostgreSQL only; Authentication: Better Auth with JWT plugin only.

### IV. Reproducibility
Entire system must be buildable from specs, plans, and prompts; No hardcoded secrets; All secrets via environment variables; System must support multiple concurrent users; Database persists data across sessions.

### V. Maintainability
RESTful API conventions must be followed consistently; Database schema changes must be traceable and version-safe; Frontend must not access data outside authenticated user context; Code generated must be readable and logically structured.

### VI. Quality Standards
API responses must use consistent JSON structures; Errors must return meaningful HTTP status codes; Frontend must be responsive and mobile-friendly; No unused endpoints, models, or components; All endpoints require valid JWT after authentication is enabled.

## Additional Constraints

Technology stack requirements:
- Backend: Python FastAPI + SQLModel only
- Frontend: Next.js 16+ App Router only
- Database: Neon Serverless PostgreSQL only
- Authentication: Better Auth with JWT plugin only
- No manual coding allowed (Claude Code only)

Deployment policies:
- Entire application can be rebuilt from specs and plans alone
- System must support multiple concurrent users
- All functionality must be explicitly defined in specs before implementation

## Security Requirements

Authentication and authorization:
- Unauthorized requests return HTTP 401
- Authenticated users can only read/write their own tasks
- JWT signature verification required on backend
- JWT expiration respected and enforced
- User ID from JWT must match request context

Data protection:
- Users can only see and modify their own tasks
- Authenticated users can only read/write their own tasks
- Frontend must not access data outside authenticated user context

## Quality Standards

Code quality:
- API responses must use consistent JSON structures
- Errors must return meaningful HTTP status codes
- Code generated must be readable and logically structured
- No unused endpoints, models, or components

User experience:
- Frontend must be responsive and mobile-friendly
- All CRUD task operations work end-to-end
- Users can sign up and sign in successfully
- JWT tokens are issued, transmitted, and verified correctly

## Success Criteria

Functional requirements:
- Users can sign up and sign in successfully
- JWT tokens are issued, transmitted, and verified correctly
- Users can only see and modify their own tasks
- All CRUD task operations work end-to-end
- Database persists data across sessions

Architecture requirements:
- Entire application can be rebuilt from specs and plans alone
- Passes hackathon review for correctness, security, and architecture
- All functionality must be explicitly defined in specs before implementation
- All API endpoints must enforce authentication and user ownership

## Governance

This constitution supersedes all other practices and guides all development decisions for the Multi-user Todo Full-Stack Web Application project. All development must comply with the principles and requirements outlined above.

Amendment procedure:
- Changes to this constitution require explicit documentation and approval
- Major changes must include a migration plan for existing implementations
- All PRs and reviews must verify compliance with these principles

Versioning policy:
- MAJOR: Backward incompatible governance/principle removals or redefinitions
- MINOR: New principle/section added or materially expanded guidance
- PATCH: Clarifications, wording, typo fixes, non-semantic refinements

Compliance review expectations:
- All implementations must be reviewed for adherence to the principles
- Regular audits should verify that the codebase follows the specified technology stack
- Security requirements must be validated during each release cycle

**Version**: 1.1.0 | **Ratified**: 2026-01-09 | **Last Amended**: 2026-01-09
