# Change Request

## Feedback from: Product Manager (internal stakeholder)

Teams are asking for a way to set due dates on tasks and get notified when a task is overdue. Right now there's no concept of deadlines in TaskFlow, so tasks just sit in "in_progress" indefinitely with no visibility into what's late.

## What they want

1. Ability to set an optional due date when creating or editing a task.
2. A visual indicator on the task list showing which tasks are overdue (past due date and not in "done" status).
3. A daily email digest sent to task assignees listing their overdue tasks.
4. A new API endpoint to fetch all overdue tasks across projects for the authenticated user.
5. Due dates should be optional — existing tasks without due dates should continue to work as before.

## Constraints

- The email digest should run as a background job, not block API requests.
- Don't change the existing status workflow — due dates are informational, not blocking.
- Must work with the existing JWT auth and pagination patterns.

## MVP scope

- Due date field on tasks (create + update)
- Overdue indicator on GET endpoints
- GET /api/tasks/overdue endpoint
- Email digest can come in a follow-up milestone if needed, but the API and data model should support it from day one.
