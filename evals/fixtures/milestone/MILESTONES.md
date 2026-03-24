# Milestones — RecipeBox

## Tech Stack
- Language: TypeScript
- Framework: Express.js + Prisma ORM
- Database: SQLite (dev), PostgreSQL (prod)
- Frontend: React + Vite
- Testing: Vitest + Supertest

---

## Milestone 0 — Project Setup ✅

**Branch:** milestone-0-setup
**Goal:** Scaffold the project with a working dev environment.

**Completed:** 2025-11-15

**Done when:**
- [x] Express server starts and responds to GET /health
- [x] Prisma schema initialised with SQLite
- [x] React app created with Vite and proxied to backend
- [x] Basic CI pipeline runs lint + test

---

## Milestone 1 — Recipe CRUD API

**Branch:** milestone-1-recipe-crud
**Goal:** Implement the core recipe data model and REST endpoints.

**Tasks:**
- Define Recipe model in Prisma schema (id, title, description, ingredients JSON, instructions text, servings int, prepTimeMinutes int, createdAt, updatedAt)
- Run prisma migrate to create the table
- Implement POST /api/recipes — create a recipe (validate: title required, servings > 0)
- Implement GET /api/recipes — list recipes with pagination (default 20 per page, support ?page and ?limit query params)
- Implement GET /api/recipes/:id — get single recipe by ID (404 if not found)
- Implement PUT /api/recipes/:id — update a recipe (404 if not found, validate same as create)
- Implement DELETE /api/recipes/:id — delete a recipe (404 if not found)
- Add Vitest + Supertest integration tests for all endpoints

**Done when:**
- [ ] Prisma migration creates the recipes table with all specified columns
- [ ] POST /api/recipes returns 201 with the created recipe; returns 400 if title is missing or servings ≤ 0
- [ ] GET /api/recipes returns paginated results; default page size is 20
- [ ] GET /api/recipes/:id returns 200 with the recipe or 404
- [ ] PUT /api/recipes/:id returns 200 with updated recipe or 404; validates input
- [ ] DELETE /api/recipes/:id returns 204 or 404
- [ ] All integration tests pass via `npm test`

---

## Milestone 2 — Recipe Search and Tags

**Branch:** milestone-2-search-tags
**Goal:** Add tagging and full-text search to recipes.

**Tasks:**
- Add Tag model (id, name unique) and RecipeTag join table
- Add GET /api/recipes?search=term — full-text search on title and description
- Add GET /api/recipes?tag=tagname — filter by tag
- Add POST /api/recipes/:id/tags — add tags to a recipe
- Add GET /api/tags — list all tags with recipe count
- Add tests for search and tag endpoints

**Done when:**
- [ ] Recipes can be tagged via POST /api/recipes/:id/tags
- [ ] GET /api/recipes?search=pasta returns recipes matching "pasta" in title or description
- [ ] GET /api/recipes?tag=italian filters by tag
- [ ] GET /api/tags returns all tags with counts
- [ ] Search and tag filters can be combined
- [ ] All tests pass
