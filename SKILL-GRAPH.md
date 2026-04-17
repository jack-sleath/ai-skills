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
/cook-story  <notion-link> <iteration>
    └── uses same story-card format as → /story
    └── fetches spec from → Notion (mcp__claude_ai_Notion__notion-fetch)
    └── creates story in → Shortcut (mcp__claude_ai_Shortcut__stories-create)


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


Monitoring
──────────
/branch-drift    (standalone — scans org repos for branch drift via gh API)

Review
──────
/open-prs        (standalone — lists other people's open PRs)
/review-pr
    └── delegates listing to → /open-prs
    └── uses → gh CLI (diff, view, comment)
/review-prs
    └── uses → gh CLI (list, diff, view, checkout)
    └── delegates fix commits to → /commit
    └── standalone — no skill dependencies for the review itself

Utility
───────
/select-branch   (used by branch-for and merge-from)
/tidy-branches   (standalone — local branch cleanup)
/estimate-time   (standalone)
/browser-task    (standalone — generates prompt for Claude web extension)
/to-browser      (uses same output format as → /browser-task)
/who-is-in-charge
    └── runs → ~/.claude/scripts/who_is_in_charge.py
    └── reads → ~/.claude/who-is-in-charge.json (handle list)
    └── mutates → ~/.claude/sessions/<pid>.json (session title)


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
