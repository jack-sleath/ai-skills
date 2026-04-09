You are reverse-engineering documentation for an existing codebase. Your job is to produce an `ACCEPTANCE_CRITERIA.md` and a `MILESTONES.md` (starting at Milestone 0) that describe what the project **currently** does, derived from its Swagger/OpenAPI definitions, unit tests, and any Gherkin scenarios the user provides.

---

## Phase 1 — Discover the project scope

Scan the working directory for Visual Studio solution files (`*.sln`), searching up to 3 levels deep.

**If multiple `.sln` files are found:**
Ask the user (one question):
> I found the following Visual Studio solutions. Which would you like to audit?
> 1. `SolutionA.sln`
> 2. `SolutionB.sln`
> 3. All of them
> 4. Other — let me specify

**If exactly one `.sln` is found:**
Announce it and ask:
> I found `SolutionName.sln`. I'll audit all projects within it. Is that correct, or would you like to limit the scope?
> 1. Yes, audit all projects in the solution
> 2. Only some projects — let me specify which
> 3. Other — let me specify

**If no `.sln` is found:**
Treat the entire working directory as a single project. Tell the user and continue.

For each project to audit, identify:
- The project name (from the `.csproj` file name, folder name, or directory name)
- The project root folder

---

## Phase 2 — Locate Swagger / OpenAPI definitions

For each project in scope, search for OpenAPI/Swagger files:
- Common filenames: `swagger.json`, `openapi.json`, `swagger.yaml`, `openapi.yaml`
- Any JSON/YAML files containing `"openapi":`, `"swagger":`, or `openapi:` at the top level
- Generated files in `wwwroot/`, `docs/`, `api/`, or `obj/` folders
- Also look for `[ApiController]` annotated controllers and Swashbuckle/NSwag configuration

Tell the user what was found for each project. If nothing was found, ask:
> I couldn't find a Swagger/OpenAPI definition for `<ProjectName>`. Where should I look?
> 1. It's generated at runtime — point me to the controllers instead
> 2. I'll paste the path
> 3. Skip Swagger for this project

If directed to controllers, read the controller files and their action methods to infer the API surface.

---

## Phase 3 — Locate unit tests

For each project in scope, search for test files:
- Projects with names matching `*.Tests`, `*.Test`, `*.Specs`, `*.UnitTests`, `*.IntegrationTests`
- Files matching `*Tests.cs`, `*Test.cs`, `*Spec.cs`, `*Fixture.cs`
- Common test frameworks: xUnit (`[Fact]`, `[Theory]`), NUnit (`[Test]`, `[TestCase]`), MSTest (`[TestMethod]`)

Read a representative sample of test files to extract:
- What behaviours are being tested (method names, test names, arrange/act/assert patterns)
- Happy path vs. edge case coverage
- Any domain concepts or business rules implied by the tests

Tell the user what was found. If nothing was found, note this and continue.

---

## Phase 4 — Gherkin input (optional)

Ask the user (one question):
> Do you have any Gherkin scenarios from existing UI or API tests to include in the acceptance criteria?
> 1. Yes — I'll paste them now
> 2. No — skip this step

If yes, ask them to paste all Gherkin scenarios. Wait for their input, then continue.

---

## Phase 5 — Generate output files

For each project being audited, generate two files. Place them in the project's root folder (e.g. `src/MyApi/ACCEPTANCE_CRITERIA.md`). If there is only one project and no solution, place them in the working directory root.

---

### File 1: `ACCEPTANCE_CRITERIA.md`

Derive the content from the Swagger definitions, unit tests, and any Gherkin provided. Do not invent behaviour — only document what is evidenced in the source material.

```
# Acceptance Criteria — <Project Name>

> **Note:** This document was generated from the existing codebase. It describes what the project currently does, not what it should do. Review and amend as needed.

## Overview
<1–2 sentences describing what this project is and its primary purpose, inferred from the API surface and test coverage>

## Target User / Consumer
<Who calls this API or uses this service — inferred from context, or "Unknown — requires manual review">

## Tech Stack
- Language: <detected from project files>
- Framework(s): <detected — e.g. ASP.NET Core, Entity Framework>
- Test framework(s): <detected — e.g. xUnit, NUnit>
- API documentation: <detected — e.g. Swashbuckle/Swagger>

## API Surface
<Only include this section if Swagger/OpenAPI or controllers were found>
A summary of the documented endpoints grouped by tag or controller:

### <Controller/Tag Name>
- `GET /path` — <summary from Swagger or inferred from controller action>
- `POST /path` — <summary>
- ...

## Functional Requirements
A numbered list of "The system must..." or "The user/caller can..." statements, derived from the API endpoints and unit tests.

1. The system must ...
2. The caller can ...
...

## Non-Functional Requirements
<Only include items evidenced in the codebase — e.g. authentication schemes found, validation attributes, error handling patterns>

## Gherkin Scenarios
<Only include this section if Gherkin was provided>

<paste the Gherkin scenarios here, formatted as Feature/Scenario blocks>

## Coverage Gaps
List any areas that appear untested or undocumented based on the audit:
- [ ] <gap or assumption requiring manual review>
```

---

### File 2: `MILESTONES.md`

```
# Milestones — <Project Name>

## Tech Stack
- Language: ...
- Framework(s): ...
- Database: ...
- Hosting/Infrastructure: <Unknown — requires manual review, or inferred from appsettings/Dockerfile>

---

## Milestone 0 — Current State Audit ✅

**Goal:** Document what the project currently does as a baseline before any new development begins.

**Completed:** <today's date>

**What exists:**
- <bullet list of what was found — e.g. "REST API with N endpoints across M controllers", "xUnit test suite with N tests", "Swagger/OpenAPI spec present">

**API surface summary:**
- <list of endpoint groups or controllers and their purpose>

**Test coverage summary:**
- <what is tested and at what level>

**Known gaps:**
- <anything flagged in the Coverage Gaps section of ACCEPTANCE_CRITERIA.md>

**Done when:**
- [x] Existing codebase has been reviewed
- [x] ACCEPTANCE_CRITERIA.md reflects current behaviour
- [x] Known coverage gaps have been identified

---

## Milestone 1 — <Next planned milestone>
> ⚠️ This milestone has not been planned yet.
```

---

## Phase 6 — Summary

After writing all files, tell the user:
- Which files were created and where
- How many endpoints and tests were found per project
- What gaps or assumptions were flagged for manual review
