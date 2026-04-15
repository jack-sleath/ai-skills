#!/usr/bin/env python3
"""Check all repos in an org/user for branches that have drifted ahead of their downstream.

Usage:
    python branch_drift.py

Requires the GitHub CLI (gh) to be installed and authenticated.
Output: Markdown grouped list of repos with drift.
"""

import io
import json
import subprocess
import sys

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def gh(*args: str) -> str:
    result = subprocess.run(
        ["gh", *args],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def gh_json(*args: str) -> list | dict:
    raw = gh(*args)
    if not raw:
        return []
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return []


def ahead_by(owner: str, repo: str, base: str, head: str) -> int:
    """Return how many commits head is ahead of base. -1 if comparison fails."""
    raw = gh(
        "api",
        f"repos/{owner}/{repo}/compare/{base}...{head}",
        "--jq", ".ahead_by",
    )
    try:
        return int(raw)
    except (ValueError, TypeError):
        return -1


def list_branches(owner: str, repo: str) -> list[str]:
    """List all branch names for a repo."""
    # --jq with --paginate returns newline-separated strings, not JSON
    result = gh(
        "api",
        f"repos/{owner}/{repo}/branches",
        "--paginate",
        "--jq", ".[].name",
    )
    return [b.strip() for b in result.splitlines() if b.strip()]


def main():
    owner = gh("repo", "view", "--json", "owner", "--jq", ".owner.login")
    if not owner:
        print("Error: could not determine repo owner. Is gh authenticated?", file=sys.stderr)
        sys.exit(1)

    repos = gh_json("repo", "list", owner, "--no-archived", "--limit", "200", "--json", "name,defaultBranchRef")
    if not repos:
        print(f"No repositories found for **{owner}**.")
        sys.exit(0)

    main_ahead_develop = []
    release_ahead_main = []
    develop_ahead_uat = []

    for repo in repos:
        name = repo["name"]
        default_branch = repo.get("defaultBranchRef", {}).get("name", "main")
        branches = list_branches(owner, name)
        branch_set = set(branches)

        # main/master ahead of develop
        if "develop" in branch_set:
            n = ahead_by(owner, name, "develop", default_branch)
            if n > 0:
                main_ahead_develop.append((name, default_branch, n))

        # release branches ahead of main/master
        release_branches = [b for b in branches if b.startswith("release/") or b.startswith("release-")]
        for rb in release_branches:
            n = ahead_by(owner, name, default_branch, rb)
            if n > 0:
                release_ahead_main.append((name, rb, n))

        # develop ahead of UAT/main
        if "develop" in branch_set and "UAT/main" in branch_set:
            n = ahead_by(owner, name, "UAT/main", "develop")
            if n > 0:
                develop_ahead_uat.append((name, n))

    total = len(main_ahead_develop) + len(release_ahead_main) + len(develop_ahead_uat)

    if total == 0:
        print(f"**All branches are in sync across {owner}.**")
        sys.exit(0)

    if main_ahead_develop:
        print("### main/master ahead of develop\n")
        for name, default_branch, n in sorted(main_ahead_develop):
            print(f"- **{name}** — {n} commits ahead ({default_branch} → develop)")
        print()

    if release_ahead_main:
        print("### Release branches ahead of main/master\n")
        for name, rb, n in sorted(release_ahead_main):
            print(f"- **{name}** `{rb}` — {n} commits ahead")
        print()

    if develop_ahead_uat:
        print("### develop ahead of UAT/main\n")
        for name, n in sorted(develop_ahead_uat):
            print(f"- **{name}** — {n} commits ahead")
        print()

    # Count unique repos with drift
    drifted_repos = set()
    for name, *_ in main_ahead_develop:
        drifted_repos.add(name)
    for name, *_ in release_ahead_main:
        drifted_repos.add(name)
    for name, *_ in develop_ahead_uat:
        drifted_repos.add(name)

    print(f"**{len(drifted_repos)} repos with drift across {owner}**")


if __name__ == "__main__":
    main()
