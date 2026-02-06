# Data Model: TaskBox Chatbot Assistant

## Entities

### Taskie (AI Chatbot Assistant)
- **Description**: The AI chatbot assistant that interacts with users and manages their tasks
- **Responsibilities**:
  - Understand and perform CRUD operations on todos
  - Provide guidance and planning suggestions
  - Maintain friendly, cheerful, and motivational personality
  - Handle user requests appropriately with proper feedback

### Todo Task
- **Description**: Represents a user's task with properties like title, description, completion status, priority, and due date
- **Fields**:
  - `id` (UUID): Unique identifier for the task
  - `user_id` (foreign key): Links the task to a specific user
  - `title` (string, required): The main title/description of the task
  - `description` (string, optional): Additional details about the task
  - `is_completed` (boolean): Indicates whether the task is completed
  - `priority` (enum): Values: Low | Medium | High
  - `category` (enum): Values: Work | Personal | Study | Custom
  - `due_date` (date): Deadline for the task completion
  - `created_at` (timestamp): When the task was created
  - `updated_at` (timestamp): When the task was last updated

### User Session
- **Description**: Represents an ongoing conversation between a user and Taskie where context is maintained
- **Fields**:
  - `session_id` (UUID): Unique identifier for the session
  - `user_id` (foreign key): Links the session to a specific user
  - `started_at` (timestamp): When the session started
  - `last_interaction_at` (timestamp): When the last interaction occurred
  - `context_data` (JSON): Stores conversation context and current task list
  - `is_active` (boolean): Indicates if the session is currently active

## Relationships
- A User can have many Todo Tasks (one-to-many via user_id foreign key)
- A User can have many User Sessions (one-to-many via user_id foreign key)
- Taskie operates on Todo Tasks and User Sessions but is not stored as a persistent entity

## State Transitions
- Todo Task: `is_completed` can transition from `false` to `true` when marked as completed
- User Session: `is_active` can transition from `true` to `false` when session ends

## Validation Rules
- Todo Task title is required and must not be empty
- Todo Task priority must be one of the allowed values (Low, Medium, High)
- Todo Task category must be one of the allowed values (Work, Personal, Study) or custom
- Due date must be a valid date in the future or past
- User ID must reference an existing user in the system