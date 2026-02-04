---
id: 1
title: Update Taskie Integration
stage: constitution
date_iso: 2026-01-16
surface: agent
model: Qwen
feature: taskie-integration
branch: main
user: user
command: /sp.constitution
labels: ["frontend", "integration", "ui", "taskie"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
  - ".specify/templates/plan-template.md"
  - ".specify/templates/spec-template.md"
  - ".specify/templates/tasks-template.md"
tests_yaml: []
prompt_text: |
  /sp.constitution 
  You are NOT creating a new chatbot.

  The chatbot "Taskie" is ALREADY IMPLEMENTED and is accessible via the backend API endpoint /chat.

  Your responsibility is ONLY to integrate the existing Taskie chatbot into the frontend UI of the Todo App "TaskBox".

  Constitution Rules:

  1. Do NOT create any chatbot logic, AI logic, or backend code.
  2. Do NOT modify the existing /chat endpoint.
  3. Do NOT create a new chat page.
  4. Taskie must appear ONLY as a floating chatbot UI on the dashboard page.
  5. The dashboard and existing todo functionality MUST remain unchanged.
  6. The chatbot UI must be clean, modern, and match the TaskBox theme.
  7. Your output must be frontend UI code only.
  8. Taskie must communicate with the backend ONLY through /chat.
response_text: |
  Updated the project constitution to reflect frontend-only integration requirements for Taskie.
  - Modified the constitution to emphasize frontend UI implementation only
  - Added Frontend Integration Requirements section
  - Updated version to 1.2.0 with amendment date
  - Updated dependent templates (plan, spec, tasks) to align with new constitution
  - Ensured all requirements from user prompt are reflected in the documentation
outcome: |
  Successfully updated the constitution and dependent templates to reflect the frontend-only
  integration requirements for Taskie. The constitution now clearly specifies that Taskie
  should be implemented as a floating chatbot UI on the dashboard page only, without any
  backend modifications.
evaluation: |
  The constitution update is complete and all dependent templates have been modified
  to align with the new requirements. The version has been incremented appropriately
  and the amendment date reflects today's date.
---