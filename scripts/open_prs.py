#!/usr/bin/env python3
"""List open PRs across an org/user (excluding your own) from the last 3 weeks.

Usage:
    python open_prs.py

Requires the GitHub CLI (gh) to be installed and authenticated.
Output: Markdown table with PR link, repo, date, source, target, author, +/- lines.
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta


def gh(*args: str) -> str:
    result = subprocess.run(
        ["gh", *args],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"Error running gh {' '.join(args)}: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def count_diff_lines(owner: str, repo: str, number: int) -> tuple[int, int]:
    """Count added/removed lines from a PR diff."""
    result = subprocess.run(
        ["gh", "pr", "diff", str(number), "--repo", f"{owner}/{repo}", "--patch"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return 0, 0

    added = 0
    removed = 0
    for line in result.stdout.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            added += 1
        elif line.startswith("-") and not line.startswith("---"):
            removed += 1
    return added, removed


def main():
    # Get current user
    me = gh("api", "user", "--jq", ".login")

    # Get owner of current repo
    owner = gh("repo", "view", "--json", "owner", "--jq", ".owner.login")

    # Date cutoff: 3 weeks ago
    cutoff = (datetime.now() - timedelta(weeks=3)).strftime("%Y-%m-%d")

    # Search for open PRs across the org
    raw = gh(
        "search", "prs",
        "--owner", owner,
        "--state", "open",
        "--created", f">={cutoff}",
        "--limit", "100",
        "--json", "number,title,url,createdAt,headRefName,baseRefName,author,repository",
    )

    prs = json.loads(raw) if raw else []

    # Filter out own PRs
    prs = [pr for pr in prs if pr.get("author", {}).get("login", "") != me]

    if not prs:
        print(f"No open PRs by others across **{owner}** in the last 3 weeks.")
        sys.exit(0)

    # Sort oldest first
    prs.sort(key=lambda pr: pr.get("createdAt", ""))

    # Build table
    print(f"| PR | Repo | Date | Source | Target | Author | Added | Removed |")
    print(f"|---|---|---|---|---|---|---|---|")

    total_added = 0
    total_removed = 0

    for pr in prs:
        number = pr["number"]
        title = pr["title"]
        url = pr["url"]
        date = pr["createdAt"][:10]
        head = pr.get("headRefName", "?")
        base = pr.get("baseRefName", "?")
        author = pr.get("author", {}).get("login", "?")
        repo_name = pr.get("repository", {}).get("name", "?")

        added, removed = count_diff_lines(owner, repo_name, number)
        total_added += added
        total_removed += removed

        print(f"| [#{number} {title}]({url}) | `{repo_name}` | {date} | `{head}` | `{base}` | @{author} | +{added} | -{removed} |")

    print(f"\n**{len(prs)} open PRs by others across {owner} in the last 3 weeks — +{total_added} / -{total_removed} lines total**")


if __name__ == "__main__":
    main()
