# TaskFlow — Lightweight Task Management API

## Target User

Small development teams (2–10 people) who need a simple, self-hosted task tracker without the overhead of Jira or Azure DevOps.

## Overview

TaskFlow is a REST API for managing tasks within projects. Teams create projects, add tasks with priorities and assignees, and track progress through customisable statuses. The API is designed to be simple enough to integrate with any front-end or CLI tool.

## Functional Requirements

- **Projects:** CRUD operations on projects (name, description, created date).
- **Tasks:** CRUD operations on tasks within a project (title, description, status, priority, assignee, due date).
- **Statuses:** Default statuses are To Do, In Progress, and Done. Projects can define custom statuses.
- **Priorities:** Tasks have a priority of Low, Medium, High, or Critical.
- **Filtering:** List tasks filtered by status, priority, assignee, or due-date range.
- **Assignment:** Assign a task to a user by email address; reassignment is allowed.
- **Comments:** Add and list comments on a task (author, body, timestamp).
- **Audit log:** Every create, update, and delete is recorded with a timestamp, actor, and before/after snapshot.

## Non-Functional Requirements

- Response time ≤ 200 ms at p95 for list endpoints with up to 500 tasks.
- API must return consistent JSON:API-style error responses.
- Authentication via API key in the `X-Api-Key` header.
- Rate limit of 100 requests per minute per API key.
- All endpoints must be documented with OpenAPI 3.1.

## Out of Scope

- Front-end UI (API-only for now).
- Real-time push notifications / WebSockets.
- File attachments on tasks.
