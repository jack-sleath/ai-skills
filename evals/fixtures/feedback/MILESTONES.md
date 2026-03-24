# Milestones — TaskFlow

## Tech Stack
- Language: C# / .NET 8
- Framework: ASP.NET Core Web API
- Database: PostgreSQL via Entity Framework Core
- Hosting: Azure App Service

---

## Milestone 0 — Current State Audit ✅

**Goal:** Document what the project currently does as a baseline.

**Completed:** 2025-12-01

**What exists:**
- REST API with 10 endpoints across 2 controllers (Projects, Tasks)
- xUnit test suite with 24 tests
- Swagger/OpenAPI spec present

**Done when:**
- [x] Existing codebase has been reviewed
- [x] ACCEPTANCE_CRITERIA.md reflects current behaviour
- [x] Known coverage gaps have been identified

---

## Milestone 1 — Task Comments ✅

**Branch:** milestone-1-task-comments
**Goal:** Allow users to add and view comments on tasks.

**Tasks:**
- Add Comment entity and migration
- Add POST /api/tasks/{id}/comments endpoint
- Add GET /api/tasks/{id}/comments endpoint
- Add unit tests for comment creation and retrieval

**Done when:**
- [x] Users can add a comment to a task via POST
- [x] Users can retrieve comments for a task via GET, ordered by creation date
- [x] Comments are validated (non-empty body, max 2000 chars)
- [x] Unit tests pass

---

## Milestone 2 — Task Assignments ✅

**Branch:** milestone-2-task-assignments
**Goal:** Support assigning multiple users to a task and notifying them.

**Tasks:**
- Add TaskAssignment join table and migration
- Add PUT /api/tasks/{id}/assignees endpoint
- Send email notification when a user is assigned
- Add unit tests

**Done when:**
- [x] Tasks can have multiple assignees
- [x] Assignees receive email notification on assignment
- [x] Removing an assignee does not trigger a notification
- [x] Unit tests pass
