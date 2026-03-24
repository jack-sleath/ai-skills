# Acceptance Criteria — TaskFlow

> **Note:** This document was generated from the existing codebase. It describes what the project currently does.

## Overview
TaskFlow is a lightweight project management API that allows teams to create projects, manage tasks within them, and track progress through status transitions.

## Target User / Consumer
Internal development teams using the API via a React frontend.

## Tech Stack
- Language: C# / .NET 8
- Framework: ASP.NET Core Web API
- Database: PostgreSQL via Entity Framework Core
- Test framework: xUnit
- API documentation: Swashbuckle/Swagger

## API Surface

### Projects
- `GET /api/projects` — List all projects for the authenticated user
- `POST /api/projects` — Create a new project
- `GET /api/projects/{id}` — Get project details including task summary
- `PUT /api/projects/{id}` — Update project name and description
- `DELETE /api/projects/{id}` — Archive a project (soft delete)

### Tasks
- `GET /api/projects/{projectId}/tasks` — List tasks in a project with optional status filter
- `POST /api/projects/{projectId}/tasks` — Create a task
- `PUT /api/tasks/{id}` — Update task details
- `PATCH /api/tasks/{id}/status` — Transition task status (todo → in_progress → review → done)
- `DELETE /api/tasks/{id}` — Delete a task

## Functional Requirements
1. The user can create a project with a name and optional description.
2. The user can view all their projects in a list.
3. The user can create tasks within a project with a title, description, and assignee.
4. Tasks follow a status workflow: todo → in_progress → review → done.
5. Invalid status transitions are rejected with a 400 error.
6. Deleting a project archives it (soft delete); its tasks remain accessible read-only.
7. The user can filter tasks by status.

## Non-Functional Requirements
- JWT-based authentication on all endpoints.
- Input validation via data annotations on all request models.
- Pagination on list endpoints (default page size: 20).

## Coverage Gaps
- [ ] No tests for pagination edge cases
- [ ] No integration tests for the soft-delete cascade behaviour
- [ ] Error response format is inconsistent between controllers
