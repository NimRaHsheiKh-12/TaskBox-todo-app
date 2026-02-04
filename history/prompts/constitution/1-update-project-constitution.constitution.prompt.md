---
id: 1
title: Update Project Constitution
stage: constitution
date: 2026-01-01
surface: agent
model: Qwen
feature: none
branch: main
user: User
command: /sp.constitution
labels: ["constitution", "governance", "spec"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - .specify/templates/plan-template.md
 - .specify/templates/spec-template.md
 - .specify/templates/tasks-template.md
tests:
 - none
---

## Prompt

```
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are updating the project constitution at `.specify/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

Follow this execution flow:

1. Load the existing constitution template at `.specify/memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `.specify/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `.specify/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - Read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - Read each command file in `.specify/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
   - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`, or agent-specific guidance files if present). Update references to principles changed.

5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Templates requiring updates (✅ updated / ⚠ pending) with file paths
   - Follow-up TODOs if any placeholders intentionally deferred.

6. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

7. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

Do not create a new template; always operate on the existing `.specify/memory/constitution.md` file.

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.


/sp.constitution 
You are operating under a Spec+ workflow.
BackendAgent and FrontendAgent are already registered with their respective skills.

This document defines the CONSTITUTION of the application.
DO NOT implement features yet.
DO NOT generate code.
This constitution will be used as the single source of truth
for all future Spec+ tasks.

========================================
APPLICATION CONSTITUTION
========================================

APPLICATION NAME:
Authenticated Full-Stack Todo Application

PURPOSE:
The purpose of this application is to provide a secure, multi-user,
full-stack Todo management system where users can manage tasks efficiently
with advanced features such as authentication, filtering, prioritization,
and due-date alerts.

----------------------------------------
ARTICLE 1 — ACCESS & AUTHENTICATION
----------------------------------------
1. The application MUST require authentication before any task interaction.
2. Users MUST sign up and log in using secure credentials.
3. JWT-based authentication MUST be used.
4. Each user MUST only be able to access their own tasks.
5. Unauthorized access to task resources MUST be blocked.

----------------------------------------
ARTICLE 2 — TASK OWNERSHIP
----------------------------------------
1. Every task MUST belong to exactly one authenticated user.
2. Tasks MUST NOT be visible across users.
3. All backend operations MUST enforce user-scoped data access.

----------------------------------------
ARTICLE 3 — TASK DATA MODEL
----------------------------------------
Each task MUST contain the following fields:

- id (UUID)
- user_id (foreign key)
- title (required)
- description (optional)
- is_completed (boolean)
- priority (Low | Medium | High)
- category (Work | Personal | Study | Custom)
- due_date (date)
- created_at (timestamp)
- updated_at (timestamp)

----------------------------------------
ARTICLE 4 — CORE TASK OPERATIONS
----------------------------------------
The system MUST support:

1. Create task
2. View all tasks
3. View single task
4. Update task
5. Delete task
6. Toggle task completion (complete / incomplete)

----------------------------------------
ARTICLE 5 — SEARCH & FILTERING
----------------------------------------
The system MUST allow:

- Search tasks by title
- Filter tasks by:
  - completion status
  - priority
  - category
  - due date (today / upcoming / overdue)

----------------------------------------
ARTICLE 6 — ALERTS & UX RULES
----------------------------------------
1. Tasks due today MUST be highlighted.
2. Overdue tasks MUST trigger alerts.
3. Completed tasks MUST appear visually distinct.
4. Priority MUST be visually indicated in the UI.

----------------------------------------
ARTICLE 7 — FRONTEND RESPONSIBILITIES
----------------------------------------
FrontendAgent MUST:
- Build a responsive UI using Next.js, TypeScript, Tailwind CSS
- Create reusable components
- Handle API consumption
- Manage loading and error states
- Enforce authentication flow on the client side

----------------------------------------
ARTICLE 8 — BACKEND RESPONSIBILITIES
----------------------------------------
BackendAgent MUST:
- Implement REST APIs using FastAPI
- Handle authentication and authorization
- Enforce validation and error handling
- Implement all business logic
- Protect all task routes with JWT authentication

----------------------------------------
ARTICLE 9 — ARCHITECTURE RULES
----------------------------------------
1. No business logic in UI components.
2. No UI concerns in backend logic.
3. Backend MUST validate all input.
4. Clean separation of concerns MUST be maintained.
5. The constitution MUST be followed strictly by all Spec+ tasks.

----------------------------------------
ARTICLE 10 — SPEC+ GOVERNANCE
----------------------------------------
1. All future work MUST be done via Spec+ commands.
2. Each feature MUST be specified independently.
3. Agents MUST not act outside their assigned responsibilities.
4. This constitution MUST NOT be violated.

========================================
END OF CONSTITUTION
========================================

## Response snapshot

Successfully updated the project constitution and aligned dependent templates. The new constitution for the "Authenticated Full-Stack Todo Application" has been created with 10 core principles covering access & authentication, task ownership, data model, core operations, search & filtering, frontend & backend responsibilities, architecture rules, and governance. The following templates were updated to align with the new constitution:
1. plan-template.md: Updated Constitution Check section to reference specific constitution principles
2. spec-template.md: Updated Functional Requirements to include constitution compliance requirements
3. tasks-template.md: Updated Foundational tasks to include constitution-specific requirements
4. The constitution file now includes all required principles and governance information with version 1.0.0

## Outcome

- ✅ Impact: Created comprehensive project constitution with 10 principles and updated 3 dependent templates
- 🧪 Tests: No tests required for constitution update
- 📁 Files: Updated .specify/memory/constitution.md, .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
- 🔁 Next prompts: Ready to create feature specifications using /sp.specify
- 🧠 Reflection: The constitution provides a solid foundation for all future development with clear principles and governance structure

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin creating feature specifications based on the new constitution