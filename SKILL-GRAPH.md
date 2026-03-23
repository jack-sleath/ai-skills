# Skill Dependency Graph

Shows how skills delegate to or depend on other skills.

```
Planning & Discovery
────────────────────
/invest-idea ──────────────────────────────────────────┐
    └── suggests → /feature, /milestone, /stories      │
                                                       │
/audit ─────────────────────────────────────────────── │
    └── suggests → /invest-idea, /feedback,            │
                   /milestone, /feature                │
                                                       ▼
/feedback ─── requires files from ──────── /invest-idea
    └── delegates → /feature (for FEATURE.md update)
    └── suggests → /milestone, /ship


Documentation
─────────────
/feature ─── requires → ACCEPTANCE_CRITERIA.md + MILESTONES.md
/stories ─── requires → MILESTONES.md
    └── generates per-milestone cards using same format as → /story
/story       (standalone — no dependencies)


Implementation
──────────────
/ship
    └── delegates each milestone to → /milestone
/milestone   (standalone implementation step)
/commit      (standalone)


Branch & Merge
──────────────
/branch-uat ──────────┐
/branch-develop ──────┴──► /branch-for
                           ├── /select-branch  (if no base given)
                           └── /merge-from
                                   └── /select-branch  (if no branch given)


Utility
───────
/select-branch   (used by branch-for and merge-from)
/estimate-time   (standalone)
/browser-task    (standalone — generates prompt for Claude web extension)
/to-browser      (uses same output format as → /browser-task)
/usage-text      (standalone — runs tools/read_usage.py via Selenium)


Evolution
─────────
/evolve [command]
    └── runs → evals/run.py (API-based eval runner)
    └── reads → evals/criteria/<command>.md (scoring rubric)
    └── reads → evals/fixtures/<command>/ (test inputs)
    └── modifies → commands/<command>.md (evolved prompt)
```
