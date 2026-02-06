# Tasks: TaskBox Chatbot Assistant

**Input**: Design documents from `/specs/[003-chatbot-taskbox]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`

<!--
  ============================================================================
  IMPORTANT: The tasks below are ACTUAL tasks based on the design documents
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan
- [X] T002 Initialize Python 3.11 project with FastAPI, SQLModel, Next.js, React dependencies
- [X] T003 [P] Configure linting and formatting tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Setup database schema and migrations framework with user and task models
- [X] T005 [P] Implement JWT-based authentication/authorization framework (Constitution: Identity & Personality)
- [X] T006 [P] Setup API routing and middleware structure with authentication enforcement
- [X] T007 Create base task model with all required fields (id, user_id, title, description, is_completed, priority, category, due_date, created_at, updated_at) (Constitution: Task Data Model)
- [X] T008 Configure error handling and logging infrastructure
- [X] T009 Setup environment configuration management
- [X] T010 Implement user-scoped data access controls (Constitution: Task Ownership)
- [X] T011 Setup input validation framework for backend (Constitution: Additional Constraints)
- [X] T012 [P] Implement Taskie personality layer for user interactions (Constitution: Identity & Personality)
- [X] T013 [P] Create emoji utility module for Taskie's friendly interactions (Constitution: Identity & Personality)
- [X] T014 [P] Implement chat-style response formatter for Taskie (Constitution: Identity & Personality)
- [X] T015 [P] Create message parser utility for identifying user intents (Constitution: Core Task Operations)
- [X] T016 [P] Implement chat session management for maintaining conversation context
- [X] T017 Create chat history storage model for storing conversation history
- [X] T018 [P] Implement API endpoint structure for chat functionality
- [X] T019 [P] Create chat request/response schemas for API validation

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Task via Chat (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks through a chat interface so that they can quickly capture ideas without navigating to a separate form.

**Independent Test**: Can be fully tested by sending a message like "Add 'buy groceries'" and verifying the task appears in the list with appropriate confirmation message.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T020 [P] [US1] Contract test for POST /api/chat/process endpoint in backend/tests/test_chat.py
- [X] T021 [P] [US1] Integration test for adding task via chat in backend/tests/test_chat.py

### Implementation for User Story 1

- [X] T022 [P] [US1] Create ChatMessage model in backend/src/models/chat.py
- [X] T023 [US1] Implement ChatService in backend/src/services/chat_service.py with add task functionality
- [X] T024 [US1] Implement message parsing logic for detecting add task intent in backend/src/utils/message_parser.py
- [X] T025 [US1] Implement POST /api/chat/process endpoint in backend/src/api/chat.py
- [X] T026 [US1] Add validation and error handling for task creation
- [X] T027 [US1] Add logging for task creation operations
- [X] T028 [US1] Create ChatInterface component in frontend/src/components/ChatInterface.jsx
- [X] T029 [US1] Create ChatPage in frontend/src/pages/ChatPage.jsx
- [X] T030 [US1] Implement chat API client in frontend/src/services/chatApi.js
- [X] T031 [US1] Add UI elements for displaying chat messages and input field
- [X] T032 [US1] Connect frontend to backend chat API for task creation

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Current Tasks via Chat (Priority: P1)

**Goal**: Enable users to view their current tasks through the chat interface so that they can quickly check what they need to do.

**Independent Test**: Can be fully tested by sending a message like "Show my tasks" and verifying Taskie responds with a numbered list of current tasks.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T033 [P] [US2] Contract test for GET /api/chat/process endpoint in backend/tests/test_chat.py
- [X] T034 [P] [US2] Integration test for viewing tasks via chat in backend/tests/test_chat.py

### Implementation for User Story 2

- [X] T035 [P] [US2] Enhance ChatService in backend/src/services/chat_service.py with view tasks functionality
- [X] T036 [US2] Implement message parsing logic for detecting view tasks intent in backend/src/utils/message_parser.py
- [X] T037 [US2] Add response formatting for task lists with numbering and emojis in backend/src/services/chat_service.py
- [X] T038 [US2] Update POST /api/chat/process endpoint in backend/src/api/chat.py to handle view tasks
- [X] T039 [US2] Add validation and error handling for task viewing
- [X] T040 [US2] Add logging for task viewing operations
- [X] T041 [US2] Enhance ChatInterface component to display task lists with proper formatting
- [X] T042 [US2] Update chat API client to handle task list responses
- [X] T043 [US2] Add UI elements for displaying formatted task lists with emojis

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Task as Completed via Chat (Priority: P2)

**Goal**: Enable users to mark tasks as completed through the chat interface so that they can easily update their progress.

**Independent Test**: Can be fully tested by sending a message like "Mark 'buy groceries' as completed" and verifying the task is marked as done with appropriate feedback.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T044 [P] [US3] Contract test for PUT /api/chat/process endpoint in backend/tests/test_chat.py
- [X] T045 [P] [US3] Integration test for marking task as completed via chat in backend/tests/test_chat.py

### Implementation for User Story 3

- [X] T046 [P] [US3] Enhance ChatService in backend/src/services/chat_service.py with mark task as completed functionality
- [X] T047 [US3] Implement message parsing logic for detecting mark task as completed intent in backend/src/utils/message_parser.py
- [X] T048 [US3] Add response formatting for task completion confirmation in backend/src/services/chat_service.py
- [X] T049 [US3] Update POST /api/chat/process endpoint in backend/src/api/chat.py to handle mark task as completed
- [X] T050 [US3] Add validation and error handling for task completion
- [X] T051 [US3] Add logging for task completion operations
- [X] T052 [US3] Enhance ChatInterface component to handle task completion responses
- [X] T053 [US3] Update chat API client to handle task completion responses
- [X] T054 [US3] Add UI elements for displaying task completion confirmations

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Update/Edit Existing Task via Chat (Priority: P2)

**Goal**: Enable users to update or edit existing tasks through the chat interface so that they can refine their tasks without deleting and recreating them.

**Independent Test**: Can be fully tested by sending a message like "Change 'buy groceries' to 'buy groceries and household supplies'" and verifying the task is updated with appropriate feedback.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [X] T055 [P] [US4] Contract test for PATCH /api/chat/process endpoint in backend/tests/test_chat.py
- [X] T056 [P] [US4] Integration test for updating/editing task via chat in backend/tests/test_chat.py

### Implementation for User Story 4

- [X] T057 [P] [US4] Enhance ChatService in backend/src/services/chat_service.py with update/edit task functionality
- [X] T058 [US4] Implement message parsing logic for detecting update/edit task intent in backend/src/utils/message_parser.py
- [X] T059 [US4] Add response formatting for task update confirmations in backend/src/services/chat_service.py
- [X] T060 [US4] Update POST /api/chat/process endpoint in backend/src/api/chat.py to handle update/edit task
- [X] T061 [US4] Add validation and error handling for task updates
- [X] T062 [US4] Add logging for task update operations
- [X] T063 [US4] Enhance ChatInterface component to handle task update responses
- [X] T064 [US4] Update chat API client to handle task update responses
- [X] T065 [US4] Add UI elements for displaying task update confirmations

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Delete Task via Chat (Priority: P3)

**Goal**: Enable users to delete tasks through the chat interface so that they can remove tasks that are no longer relevant.

**Independent Test**: Can be fully tested by sending a message like "Delete 'buy groceries'" and verifying the task is removed with appropriate feedback.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [X] T066 [P] [US5] Contract test for DELETE /api/chat/process endpoint in backend/tests/test_chat.py
- [X] T067 [P] [US5] Integration test for deleting task via chat in backend/tests/test_chat.py

### Implementation for User Story 5

- [X] T068 [P] [US5] Enhance ChatService in backend/src/services/chat_service.py with delete task functionality
- [X] T069 [US5] Implement message parsing logic for detecting delete task intent in backend/src/utils/message_parser.py
- [X] T070 [US5] Add response formatting for task deletion confirmations in backend/src/services/chat_service.py
- [X] T071 [US5] Update POST /api/chat/process endpoint in backend/src/api/chat.py to handle delete task
- [X] T072 [US5] Add validation and error handling for task deletion
- [X] T073 [US5] Add logging for task deletion operations
- [X] T074 [US5] Enhance ChatInterface component to handle task deletion responses
- [X] T075 [US5] Update chat API client to handle task deletion responses
- [X] T076 [US5] Add UI elements for displaying task deletion confirmations

**Checkpoint**: At this point, User Stories 1, 2, 3, 4 AND 5 should all work independently

---

## Phase 8: User Story 6 - Receive Guidance and Suggestions (Priority: P3)

**Goal**: Enable users to receive helpful suggestions and guidance from Taskie so that they can better manage their tasks and productivity.

**Independent Test**: Can be fully tested by asking Taskie for suggestions and verifying it provides helpful guidance about task management.

### Tests for User Story 6 (OPTIONAL - only if tests requested) ⚠️

- [X] T077 [P] [US6] Contract test for guidance endpoint in backend/tests/test_chat.py
- [X] T078 [P] [US6] Integration test for receiving guidance via chat in backend/tests/test_chat.py

### Implementation for User Story 6

- [X] T079 [P] [US6] Enhance ChatService in backend/src/services/chat_service.py with guidance and suggestions functionality
- [X] T080 [US6] Implement message parsing logic for detecting guidance requests in backend/src/utils/message_parser.py
- [X] T081 [US6] Add response formatting for guidance and suggestions in backend/src/services/chat_service.py
- [X] T082 [US6] Update POST /api/chat/process endpoint in backend/src/api/chat.py to handle guidance requests
- [X] T083 [US6] Add validation and error handling for guidance responses
- [X] T084 [US6] Add logging for guidance operations
- [X] T085 [US6] Enhance ChatInterface component to handle guidance responses
- [X] T086 [US6] Update chat API client to handle guidance responses
- [X] T087 [US6] Add UI elements for displaying guidance and suggestions

**Checkpoint**: All user stories should now be independently functional

---

## Phase 9: Additional API Endpoints

**Goal**: Implement additional API endpoints for chat history and session management as defined in the contracts.

### Implementation

- [X] T088 [P] Implement GET /api/chat/history/{user_id} endpoint in backend/src/api/chat.py
- [X] T089 [P] Implement POST /api/chat/session endpoint in backend/src/api/chat.py
- [X] T090 [P] Implement DELETE /api/chat/session/{session_id} endpoint in backend/src/api/chat.py
- [X] T091 [P] Create chat history model in backend/src/models/chat_history.py
- [X] T092 [P] Create chat session model in backend/src/models/chat_session.py
- [X] T093 [P] Update ChatService to handle session management
- [X] T094 [P] Update ChatService to handle chat history retrieval
- [X] T095 [P] Add tests for additional API endpoints in backend/tests/test_chat.py

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T096 [P] Documentation updates in docs/
- [X] T097 Code cleanup and refactoring
- [X] T098 Performance optimization across all stories
- [X] T099 [P] Additional unit tests (if requested) in backend/tests/unit/ and frontend/tests/
- [X] T100 Security hardening
- [X] T101 Run quickstart.md validation
- [X] T102 [P] Add comprehensive error handling for edge cases
- [X] T103 [P] Implement fallback responses for ambiguous requests
- [X] T104 [P] Add rate limiting to chat endpoints
- [X] T105 [P] Add caching for frequently accessed data
- [X] T106 [P] Add monitoring and metrics for chat functionality

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Additional API Endpoints (Phase 9)**: Depends on foundational phase and can be done in parallel with user stories
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable
- **User Story 6 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1-US5 but should be independently testable

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
Task: "Contract test for POST /api/chat/process endpoint in backend/tests/test_chat.py"
Task: "Integration test for adding task via chat in backend/tests/test_chat.py"

# Launch all models for User Story 1 together:
Task: "Create ChatMessage model in backend/src/models/chat.py"

# Launch all implementation tasks for User Story 1 together:
Task: "Implement ChatService in backend/src/services/chat_service.py with add task functionality"
Task: "Implement message parsing logic for detecting add task intent in backend/src/utils/message_parser.py"
Task: "Implement POST /api/chat/process endpoint in backend/src/api/chat.py"
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
6. Add User Story 5 → Test independently → Deploy/Demo
7. Add User Story 6 → Test independently → Deploy/Demo
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
   - Developer F: User Story 6
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