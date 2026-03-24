# Milestones

## Milestone 1 — Project CRUD

**Goal:** Stand up the API skeleton and implement full CRUD for projects.

**Tasks:**
1. Initialise Node.js project with Express and TypeScript.
2. Set up PostgreSQL with Prisma ORM.
3. Create `projects` table (id, name, description, created_at, updated_at).
4. Implement `POST /projects`, `GET /projects`, `GET /projects/:id`, `PATCH /projects/:id`, `DELETE /projects/:id`.
5. Add request validation with Zod.
6. Write integration tests for all project endpoints.

**Done when:**
- [ ] All five project endpoints return correct status codes and bodies.
- [ ] Validation rejects missing/invalid fields with a JSON:API error response.
- [ ] Integration tests pass in CI.

---

## Milestone 2 — Tasks & Statuses

**Goal:** Add task management within projects, including custom statuses.

**Tasks:**
1. Create `tasks` table (id, project_id, title, description, status, priority, assignee_email, due_date, created_at, updated_at).
2. Seed default statuses (To Do, In Progress, Done) per project.
3. Implement CRUD endpoints under `POST /projects/:id/tasks`, etc.
4. Add `GET /projects/:id/statuses` and `POST /projects/:id/statuses` for custom statuses.
5. Validate that a task's status is one of the project's allowed statuses.
6. Write integration tests for task and status endpoints.

**Done when:**
- [ ] Tasks can be created, read, updated, and deleted within a project.
- [ ] Custom statuses can be added and are enforced on task creation/update.
- [ ] Integration tests pass.

---

## Milestone 3 — Filtering, Comments & Audit Log

**Goal:** Add advanced querying, task comments, and an audit trail.

**Tasks:**
1. Add query-parameter filtering to `GET /projects/:id/tasks` (status, priority, assignee, due_date_from, due_date_to).
2. Create `comments` table and implement `POST /tasks/:id/comments`, `GET /tasks/:id/comments`.
3. Create `audit_log` table (id, entity_type, entity_id, action, actor, before, after, timestamp).
4. Add middleware to record audit entries on every CUD operation.
5. Implement `GET /projects/:id/audit-log` with pagination.
6. Write integration tests for filtering, comments, and audit log.

**Done when:**
- [ ] Filtering returns correct subsets of tasks.
- [ ] Comments can be added and listed per task.
- [ ] Every create/update/delete is recorded in the audit log with before/after snapshots.
- [ ] Integration tests pass.

---

## Milestone 4 — Auth, Rate Limiting & OpenAPI Docs

**Goal:** Secure the API and publish machine-readable documentation.

**Tasks:**
1. Add API-key authentication middleware reading `X-Api-Key`.
2. Implement rate limiting (100 req/min per key) with `express-rate-limit`.
3. Generate OpenAPI 3.1 spec from route definitions.
4. Serve Swagger UI at `/docs`.
5. Ensure all error responses follow the JSON:API error format.
6. Write integration tests for auth, rate limiting, and error responses.

**Done when:**
- [ ] Unauthenticated requests receive 401.
- [ ] Requests exceeding the rate limit receive 429.
- [ ] `/docs` renders the full Swagger UI.
- [ ] All error responses match JSON:API format.
- [ ] Integration tests pass.
