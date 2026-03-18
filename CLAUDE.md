# Project Rules

## Adding or modifying skills

Whenever you create a new skill file in `commands/` or rename/remove an existing one, you **must** update the Skills table in `README.md` to reflect the change before committing.

Whenever you create a new skill or modify how an existing skill delegates to or depends on another skill, you **must** update `SKILL-GRAPH.md` to reflect the change before committing.

Each row in the table should follow this format:
| Skill name | `/command [args]` | One-line description of what it does |
