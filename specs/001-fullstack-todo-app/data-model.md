# Data Model: Full-Stack Todo Application with Authentication

## User Entity

**Table Name**: `users`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Not Null | Unique identifier for the user |
| email | String(255) | Unique, Not Null | User's email address |
| password_hash | String(255) | Not Null | Securely hashed password |
| created_at | DateTime | Not Null | Timestamp when user was created |
| updated_at | DateTime | Not Null | Timestamp when user was last updated |

**Relationships**:
- One-to-Many: User has many Todos (via user_id foreign key)

## Todo Entity

**Table Name**: `todos`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Not Null | Unique identifier for the todo |
| user_id | UUID | Foreign Key, Not Null | Reference to the owning user |
| title | String(255) | Not Null | Title of the todo |
| description | Text | Nullable | Detailed description of the todo |
| is_completed | Boolean | Not Null, Default: false | Completion status |
| priority | String(20) | Not Null, Check: ['Low', 'Medium', 'High'] | Priority level |
| category | String(50) | Nullable | Category for organization |
| due_date | Date | Nullable | Due date for the todo |
| created_at | DateTime | Not Null | Timestamp when todo was created |
| updated_at | DateTime | Not Null | Timestamp when todo was last updated |

**Relationships**:
- Many-to-One: Todo belongs to one User (via user_id foreign key)

## Validation Rules

### User Validation
- Email must be a valid email format
- Email must be unique across all users
- Password must be securely hashed (no plaintext storage)

### Todo Validation
- Title is required (not empty)
- Priority must be one of: 'Low', 'Medium', 'High'
- Category can be custom or one of: 'Work', 'Personal', 'Study'
- Due date must be a valid date if provided
- Todos can only be accessed by their owner

## State Transitions

### Todo Completion
- `is_completed` transitions from `false` to `true` when marked complete
- `is_completed` transitions from `true` to `false` when marked incomplete
- `updated_at` is updated on any change

## Indexes

### User Table
- Index on `email` for efficient lookups during authentication

### Todo Table
- Index on `user_id` for efficient user-scoped queries
- Index on `is_completed` for filtering by completion status
- Index on `priority` for filtering by priority
- Index on `due_date` for filtering by due date
- Composite index on (`user_id`, `is_completed`) for common queries