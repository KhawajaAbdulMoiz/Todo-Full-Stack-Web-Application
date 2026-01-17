# Task Breakdown: Frontend & UX Integration

**Input**: Design documents from `/specs/001-frontend-ux-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume web app structure - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure for frontend-ux-integration service per implementation plan
- [X] T002 Initialize Next.js project with required dependencies in frontend/
- [X] T003 [P] Configure shared environment variables for backend API URL and auth secret

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T004 Setup authentication context and session management (Better Auth with JWT) in frontend/src/lib/auth.ts
- [X] T005 [P] Implement JWT verification middleware for protected routes in frontend/src/middleware.ts
- [X] T006 [P] Setup API routing and state management structure (Next.js App Router) in frontend/src/app/
- [X] T007 Create base models/entities that all stories depend on (User, Task) in frontend/src/lib/types.ts
- [X] T008 Configure error handling and notification infrastructure in frontend/src/lib/errors.ts

**Constitution Compliance Check**:
- [ ] Verify Next.js 16+ App Router stack is used (no other frontend frameworks)
- [ ] Verify Neon Serverless PostgreSQL is used via backend API (no other databases)
- [ ] Verify Better Auth with JWT plugin is used (no other auth systems)
- [ ] Verify no manual coding (Claude Code only)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable new users to register for an account, log in, and receive a JWT token that authenticates them for subsequent requests.

**Independent Test**: Can be fully tested by registering a new user, logging in, and verifying that a valid JWT token is issued and accepted by protected endpoints.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T009 [P] [US1] Contract test for registration endpoint in frontend/tests/contract/test_auth.ts
- [ ] T010 [P] [US1] Integration test for user registration flow in frontend/tests/integration/test_auth.ts

### Implementation for User Story 1

- [X] T011 [P] [US1] Create User model in frontend/src/lib/types.ts
- [X] T012 [P] [US1] Implement authentication service in frontend/src/lib/auth.ts
- [X] T013 [US1] Implement registration endpoint integration in frontend/src/app/auth/register/actions.ts (depends on T011, T012)
- [X] T014 [US1] Implement login endpoint integration in frontend/src/app/auth/login/actions.ts (depends on T011, T012)
- [X] T015 [US1] Create registration form component in frontend/src/components/auth/register-form.tsx
- [X] T016 [US1] Create login form component in frontend/src/components/auth/login-form.tsx
- [X] T017 [US1] Implement protected route middleware in frontend/src/middleware.ts

**Security Check**:
- [ ] Verify all API endpoints enforce authentication and user ownership (handled by backend)
- [ ] Verify JWT-based authentication is verified on every backend request (handled by auth library)
- [ ] Verify authenticated users can only read/write their own tasks (enforced by backend)
- [ ] Verify no hardcoded secrets; all secrets via environment variables
- [ ] Verify user ID from JWT matches request context (enforced by backend)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Management Dashboard (Priority: P1)

**Goal**: Enable authenticated users to view, create, update, and delete their tasks with a responsive UI.

**Independent Test**: Can be fully tested by creating tasks as one user, verifying another user cannot access those tasks, and performing all CRUD operations on owned tasks.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T018 [P] [US2] Contract test for tasks endpoints in frontend/tests/contract/test_tasks.ts
- [ ] T019 [P] [US2] Integration test for task CRUD operations in frontend/tests/integration/test_tasks.ts

### Implementation for User Story 2

- [X] T020 [P] [US2] Create Task model in frontend/src/lib/types.ts (depends on T011)
- [X] T021 [US2] Implement task service in frontend/src/lib/api.ts
- [X] T022 [US2] Implement GET tasks endpoint integration in frontend/src/app/dashboard/tasks/actions.ts (depends on T020, T021)
- [X] T023 [US2] Implement POST task endpoint integration in frontend/src/app/dashboard/tasks/actions.ts (depends on T020, T021)
- [X] T024 [US2] Implement PUT/DELETE task endpoint integration in frontend/src/app/dashboard/tasks/actions.ts (depends on T020, T021)
- [X] T025 [US2] Create task list component in frontend/src/components/tasks/task-list.tsx
- [X] T026 [US2] Create task form component in frontend/src/components/tasks/task-form.tsx
- [X] T027 [US2] Create task item component in frontend/src/components/tasks/task-item.tsx

**Security Check**:
- [ ] Verify all API endpoints enforce authentication and user ownership (handled by backend)
- [ ] Verify JWT-based authentication is verified on every backend request (handled by auth library)
- [ ] Verify authenticated users can only read/write their own tasks (enforced by backend)
- [ ] Verify no hardcoded secrets; all secrets via environment variables
- [ ] Verify user ID from JWT matches request context (enforced by backend)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task Completion Toggle (Priority: P2)

**Goal**: Enable authenticated users to mark their tasks as complete or incomplete with a simple toggle action.

**Independent Test**: Can be fully tested by toggling task completion status and verifying the change is reflected in the UI and persisted in the database.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T028 [P] [US3] Contract test for toggle completion endpoint in frontend/tests/contract/test_tasks.ts
- [ ] T29 [P] [US3] Integration test for task completion flow in frontend/tests/integration/test_tasks.ts

### Implementation for User Story 3

- [X] T030 [US3] Implement PATCH task completion toggle endpoint integration in frontend/src/app/dashboard/tasks/actions.ts (depends on T020, T021)
- [X] T031 [US3] Create task completion toggle component in frontend/src/components/tasks/task-toggle.tsx
- [X] T032 [US3] Integrate toggle functionality with task item component in frontend/src/components/tasks/task-item.tsx (depends on T031)

**Security Check**:
- [ ] Verify all API endpoints enforce authentication and user ownership (handled by backend)
- [ ] Verify JWT-based authentication is verified on every backend request (handled by auth library)
- [ ] Verify authenticated users can only modify their own tasks (enforced by backend)
- [ ] Verify no hardcoded secrets; all secrets via environment variables
- [ ] Verify user ID from JWT matches request context (enforced by backend)

---

## Phase 6: User Story 4 - Responsive UI Experience (Priority: P2)

**Goal**: Ensure users can access and use the application effectively on both desktop and mobile devices with a responsive interface.

**Independent Test**: Can be fully tested by accessing the application on different screen sizes and verifying that the UI adapts appropriately.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T033 [P] [US4] Responsive UI tests in frontend/tests/ui/responsive-tests.ts

### Implementation for User Story 4

- [X] T034 [US4] Create responsive layout components in frontend/src/components/ui/layout.tsx
- [X] T035 [US4] Implement responsive design for task list in frontend/src/components/tasks/task-list.tsx
- [X] T036 [US4] Implement responsive design for task form in frontend/src/components/tasks/task-form.tsx
- [X] T037 [US4] Add mobile navigation in frontend/src/components/ui/mobile-nav.tsx

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T038 [P] Documentation updates in docs/
- [X] T039 Code cleanup and refactoring
- [X] T040 Performance optimization across all stories
- [X] T041 [P] Additional unit tests in frontend/tests/unit/
- [X] T042 Security hardening
- [X] T043 Run quickstart.md validation

**Quality Standards Check**:
- [ ] Verify API responses use consistent JSON structures
- [ ] Verify errors return meaningful HTTP status codes
- [ ] Verify frontend is responsive and mobile-friendly
- [ ] Verify code is readable and logically structured
- [ ] Verify no unused endpoints, models, or components
- [ ] Verify RESTful API conventions are followed consistently
- [ ] Verify database schema changes are traceable and version-safe
- [ ] Verify frontend does not access data outside authenticated user context
- [ ] Verify all endpoints require valid JWT after authentication is enabled

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 components
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US2 components
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Can work in parallel with other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for registration endpoint in frontend/tests/contract/test_auth.ts"
Task: "Integration test for user registration flow in frontend/tests/integration/test_auth.ts"

# Launch all models for User Story 1 together:
Task: "Create User model in frontend/src/lib/types.ts"
Task: "Implement authentication service in frontend/src/lib/auth.ts"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All functionality must be explicitly defined in specs before implementation
- No manual coding allowed - use Claude Code only
- All API endpoints must enforce authentication and user ownership (handled by backend)
- JWT signature verification required on backend (handled by auth library)
- JWT expiration respected and enforced (handled by auth library)
- User ID from JWT matches request context (enforced by backend)