---

description: "Task list for Backend API & Database (Task Management)"
---

# Tasks: Backend API & Database (Task Management)

**Input**: Design documents from `/specs/001-backend-task-api/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend-task-api/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure for backend-task-api service per implementation plan
- [X] T002 Initialize Python project with FastAPI dependencies in backend-task-api/
- [X] T003 Configure shared environment variables for database connection and JWT secret

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T004 Setup database schema and migrations framework (Neon Serverless PostgreSQL) in backend-task-api/
- [X] T005 [P] Implement JWT verification middleware for authentication in backend-task-api/src/core/security.py
- [X] T006 [P] Setup API routing and middleware structure (FastAPI) in backend-task-api/src/main.py
- [X] T007 Create base models/entities that all stories depend on (SQLModel) in backend-task-api/src/models/
- [X] T008 Configure error handling and logging infrastructure in backend-task-api/src/core/

**Constitution Compliance Check**:
- [ ] Verify Python FastAPI + SQLModel stack is used (no other backend frameworks)
- [ ] Verify Neon Serverless PostgreSQL is used (no other databases)
- [ ] Verify JWT verification is implemented on all endpoints
- [ ] Verify no manual coding - all via Claude Code

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Task Creation (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to create new tasks with title and optional description, validating input and storing tasks in the database with proper user association.

**Independent Test**: Can be fully tested by authenticating as a user, submitting a valid task creation request, and verifying that the task is stored in the database with the correct owner.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T009 [P] [US1] Contract test for task creation endpoint in backend-task-api/tests/contract/test_tasks.py
- [ ] T010 [P] [US1] Integration test for task creation flow in backend-task-api/tests/integration/test_tasks.py

### Implementation for User Story 1

- [X] T011 [P] [US1] Create Task model in backend-task-api/src/models/task.py
- [X] T012 [P] [US1] Implement task service in backend-task-api/src/services/task_service.py
- [X] T013 [US1] Implement POST task endpoint in backend-task-api/src/api/tasks.py (depends on T011, T012)
- [X] T014 [US1] Add JWT authentication validation to task creation endpoint in backend-task-api/src/api/tasks.py
- [X] T015 [US1] Implement input validation for task creation in backend-task-api/src/schemas/task.py

**Security Check**:
- [ ] Verify all API endpoints enforce authentication and user ownership
- [ ] Verify JWT-based authentication is verified on every backend request
- [ ] Verify authenticated users can only create tasks for their own account
- [ ] Verify no hardcoded secrets; all secrets via environment variables
- [ ] Verify user ID from JWT matches request context

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Retrieval (Priority: P1)

**Goal**: Enable authenticated users to retrieve only their own tasks from the system, ensuring proper user isolation.

**Independent Test**: Can be fully tested by creating tasks for multiple users, authenticating as each user, and verifying that each user only sees their own tasks.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T016 [P] [US2] Contract test for task retrieval endpoints in backend-task-api/tests/contract/test_tasks.py
- [ ] T017 [P] [US2] Integration test for task retrieval flow in backend-task-api/tests/integration/test_tasks.py

### Implementation for User Story 2

- [X] T018 [P] [US2] Extend Task model with user relationship in backend-task-api/src/models/task.py
- [X] T019 [US2] Update task service to filter by user in backend-task-api/src/services/task_service.py
- [X] T020 [US2] Implement GET tasks endpoint in backend-task-api/src/api/tasks.py (depends on T018, T019)
- [X] T021 [US2] Implement GET specific task endpoint in backend-task-api/src/api/tasks.py (depends on T018, T019)
- [X] T022 [US2] Add user ownership validation to retrieval endpoints in backend-task-api/src/api/tasks.py

**Security Check**:
- [ ] Verify all API endpoints enforce authentication and user ownership
- [ ] Verify JWT-based authentication is verified on every backend request
- [ ] Verify authenticated users can only retrieve their own tasks
- [ ] Verify no hardcoded secrets; all secrets via environment variables
- [ ] Verify user ID from JWT matches request context

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task Modification (Priority: P2)

**Goal**: Enable authenticated users to update their existing tasks, including toggling completion status, with proper ownership validation.

**Independent Test**: Can be fully tested by creating a task for a user, authenticating as that user, modifying the task, and verifying the changes are persisted.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T023 [P] [US3] Contract test for task modification endpoints in backend-task-api/tests/contract/test_tasks.py
- [ ] T024 [P] [US3] Integration test for task modification flow in backend-task-api/tests/integration/test_tasks.py

### Implementation for User Story 3

- [X] T025 [US3] Implement PUT task endpoint in backend-task-api/src/api/tasks.py (depends on T018, T019)
- [X] T026 [US3] Implement PATCH task completion toggle endpoint in backend-task-api/src/api/tasks.py (depends on T018, T019)
- [X] T027 [US3] Add update functionality to task service in backend-task-api/src/services/task_service.py
- [X] T028 [US3] Add user ownership validation to modification endpoints in backend-task-api/src/api/tasks.py

**Security Check**:
- [ ] Verify all API endpoints enforce authentication and user ownership
- [ ] Verify JWT-based authentication is verified on every backend request
- [ ] Verify authenticated users can only modify their own tasks
- [ ] Verify no hardcoded secrets; all secrets via environment variables
- [ ] Verify user ID from JWT matches request context

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Task Deletion (Priority: P2)

**Goal**: Enable authenticated users to delete their own tasks, with proper ownership validation.

**Independent Test**: Can be fully tested by creating a task for a user, authenticating as that user, deleting the task, and verifying it's removed from the database.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T029 [P] [US4] Contract test for task deletion endpoint in backend-task-api/tests/contract/test_tasks.py
- [ ] T030 [P] [US4] Integration test for task deletion flow in backend-task-api/tests/integration/test_tasks.py

### Implementation for User Story 4

- [X] T031 [US4] Implement DELETE task endpoint in backend-task-api/src/api/tasks.py (depends on T018, T019)
- [X] T032 [US4] Add delete functionality to task service in backend-task-api/src/services/task_service.py
- [X] T033 [US4] Add user ownership validation to deletion endpoint in backend-task-api/src/api/tasks.py

**Security Check**:
- [ ] Verify all API endpoints enforce authentication and user ownership
- [ ] Verify JWT-based authentication is verified on every backend request
- [ ] Verify authenticated users can only delete their own tasks
- [ ] Verify no hardcoded secrets; all secrets via environment variables
- [ ] Verify user ID from JWT matches request context

**Checkpoint**: All user stories should now be functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T034 [P] Documentation updates in docs/
- [ ] T035 Code cleanup and refactoring
- [ ] T036 Performance optimization across all stories
- [ ] T037 [P] Additional unit tests in backend-task-api/tests/unit/
- [ ] T038 Security hardening
- [ ] T039 API validation and testing with Postman

**Quality Standards Check**:
- [ ] Verify API responses use consistent JSON structures
- [ ] Verify errors return meaningful HTTP status codes
- [ ] Verify code is readable and logically structured
- [ ] Verify no unused endpoints, models, or components
- [ ] Verify RESTful API conventions are followed consistently
- [ ] Verify database schema changes are traceable and version-safe
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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US2 components
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Depends on US2 components

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
Task: "Contract test for task creation endpoint in backend-task-api/tests/contract/test_tasks.py"
Task: "Integration test for task creation flow in backend-task-api/tests/integration/test_tasks.py"

# Launch all models for User Story 1 together:
Task: "Create Task model in backend-task-api/src/models/task.py"
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
- All API endpoints must enforce authentication and user ownership
- JWT signature verification required on backend
- JWT expiration respected and enforced