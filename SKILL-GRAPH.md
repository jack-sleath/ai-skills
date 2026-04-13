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
/tidy-branches   (standalone — local branch cleanup)
/estimate-time   (standalone)
/browser-task    (standalone — generates prompt for Claude web extension)
/to-browser      (uses same output format as → /browser-task)


Roles
─────
/as-a <role> [task]
    └── reads → ~/.claude/roles/<role>.md (role definition)
    └── applies role framework to the given task
    └── available roles: qa-tester, code-reviewer, tech-lead,
        product-manager, security-auditor, devops-engineer,
        technical-writer, ux-designer


Evolution (repo-local — .claude/commands/)
──────────────────────────────────────────
/create-criteria [command(s)]
    └── reads → commands/<command>.md (to derive dimensions)
    └── creates → evals/criteria/<command>.md (scoring rubric)
    └── creates → evals/fixtures/<command>/ (sample inputs)

/evolve [command(s)]
    └── runs → evals/run.py (API-based eval runner)
    └── reads → evals/criteria/<command>.md (scoring rubric)
    └── reads → evals/fixtures/<command>/ (test inputs)
    └── modifies → commands/<command>.md (evolved prompt)
    └── spawns → Agent (worktree, one per command in parallel batch mode)
```
