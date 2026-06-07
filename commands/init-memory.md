You are setting up a persistent, two-tier wiki memory system in the current project, inspired by the LLM-maintained-wiki pattern (https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). Follow these steps in order.

The system has three parts:
- **`MEMORY.md`** (project root) — always in context via a `CLAUDE.md` import. Contains the protocol, **Core Memory** (Tier 1: facts relevant to every session), and the **Wiki Index** (Tier 2: titles + tags only).
- **`memory-wiki/`** — full wiki pages, read on demand when the index suggests relevance.
- **`CLAUDE.md`** — gains an `@MEMORY.md` import so the protocol and index load every session.

---

## Step 1 — Idempotency / repair check

Check whether `MEMORY.md` already exists in the project root.

**If it exists, do not overwrite it.** Instead, verify and repair:
1. The three sections exist: `## Memory Protocol`, `## Core Memory`, `## Wiki Index`. Restore any missing section from the template in Step 2 (preserving existing content).
2. Every Wiki Index row points at a file that exists in `memory-wiki/`. Remove rows for missing files.
3. Every `memory-wiki/*.md` file has an index row. Add rows for unindexed pages (derive title/tags from the page's frontmatter).
4. The project's `CLAUDE.md` contains the `@MEMORY.md` import block from Step 4. Add it if missing.

Report what was checked and what (if anything) was repaired, then **stop** — do not continue to the steps below.

If `MEMORY.md` does not exist, continue.

---

## Step 2 — Create `MEMORY.md`

Create `MEMORY.md` in the project root with exactly this content:

````markdown
# Project Memory

## Memory Protocol

This file is always in context. It defines how you (Claude) maintain this project's memory. The memory has two tiers:

- **Core Memory** (below) — always in context. Only for facts relevant to *every* session.
- **Wiki** (`memory-wiki/`) — full pages on disk. Only their titles + tags live in the Wiki Index below; read a page only when relevant.

### Continuous capture

After every user message and every reply you give, silently assess: does it contain durable knowledge? Durable means: decisions made, user preferences, constraints, gotchas, domain facts, or anything that was hard to figure out and would be costly to rediscover. If yes, write it to memory immediately as part of your work — do not announce routine captures or ask permission. If no, do nothing.

### Tier decision

- Core Memory holds at most **20 bullets**. Reserve it for facts that matter in *every* session.
- Everything else becomes (or extends) a wiki page.
- Over budget? Demote the least universal bullets into wiki pages.
- A wiki topic you find yourself recalling session after session? Promote its key fact to Core Memory.

### Recall

At the start of any task, scan the Wiki Index titles and tags. Read any page plausibly related to the task **before** starting work. Never inline whole pages into Core Memory — the index alone stays in context.

### Wiki page format

Pages live at `memory-wiki/<kebab-slug>.md`:

```markdown
---
title: Human-readable title
tags: [tag-one, tag-two]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

Facts, in plain prose or bullets. Cross-link related pages with [[other-slug]].
```

Update `updated` (and the index row's tags, if they changed) whenever a page changes. Use absolute dates, never relative ones.

### Index discipline

Every page create, rename, or delete must update its Wiki Index row in the same edit. The index never contains page content — titles and tags only.

### Maintenance

Whenever you touch the wiki, opportunistically lint: merge duplicate facts, delete claims that turned out to be false, fix index rows pointing at missing pages, add missing `[[cross-links]]`.

### Exclusions

- Never store secrets, credentials, or tokens.
- Never store what the code, git history, or CLAUDE.md already records.

### Git

Memory files are committed. Include `MEMORY.md` / `memory-wiki/` changes in commits alongside the work that produced them.

## Core Memory

<!-- Max 20 bullets. Only facts relevant to every session. -->

## Wiki Index

| Title | Tags | File |
|---|---|---|
````

---

## Step 3 — Create the wiki directory

Create `memory-wiki/` in the project root with a `.gitkeep` file so the empty directory is committable. (If Step 5 seeds pages, the `.gitkeep` is unnecessary but harmless.)

---

## Step 4 — Wire the import into `CLAUDE.md`

If the project has no `CLAUDE.md`, create one. Then append this block (skip if it already exists):

```
<!-- init-memory:start -->
@MEMORY.md
<!-- init-memory:end -->
```

Never duplicate the block, and never modify anything else in an existing `CLAUDE.md`.

---

## Step 5 — Offer to seed

Ask the user whether to do an initial capture pass. If yes:
- Scan the current conversation for durable facts (decisions, preferences, constraints already stated).
- Scan the project — README, recent commit messages, obvious conventions — for knowledge that is *not* derivable from a quick look at the code (skip anything CLAUDE.md or the code already records, per the exclusions).
- Write Core Memory bullets and/or wiki pages + index rows accordingly.

If no, leave the system empty.

---

## Step 6 — Summary

Report:
- What was created (`MEMORY.md`, `memory-wiki/`, the `CLAUDE.md` import) and anything seeded.
- That memory files should be committed with the project.
- That the import loads automatically from the **next** session, but you will follow the protocol immediately in this one.
