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
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

GRAPHQL_QUERY = """
query($owner: String!, $cursor: String) {
  %s(login: $owner) {
    repositories(first: 100, after: $cursor, isArchived: false) {
      pageInfo { hasNextPage endCursor }
      nodes {
        name
        defaultBranchRef { name }
        develop: ref(qualifiedName: "refs/heads/develop") { name }
        uatMain: ref(qualifiedName: "refs/heads/UAT/main") { name }
        releaseBranches: refs(refPrefix: "refs/heads/release/", first: 20) {
          nodes { name }
        }
      }
    }
  }
}
"""

TOKEN = None


def get_token() -> str:
    global TOKEN
    if TOKEN is None:
        result = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            print("Error: could not get GitHub token. Is gh authenticated?", file=sys.stderr)
            sys.exit(1)
        TOKEN = result.stdout.strip()
    return TOKEN


def gh_api(path: str) -> dict | None:
    """Make a direct GitHub REST API call, bypassing gh CLI overhead."""
    url = f"https://api.github.com/{path}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {get_token()}",
        "Accept": "application/vnd.github+json",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError:
        return None


def gh_graphql(query: str, variables: dict) -> dict:
    """Make a direct GitHub GraphQL API call."""
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Authorization": f"Bearer {get_token()}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError:
        return {}


def ahead_by(owner: str, repo: str, base: str, head: str) -> int:
    """Return how many commits head is ahead of base. -1 if comparison fails."""
    base_enc = urllib.parse.quote(base, safe="")
    head_enc = urllib.parse.quote(head, safe="")
    data = gh_api(f"repos/{owner}/{repo}/compare/{base_enc}...{head_enc}")
    if data and "ahead_by" in data:
        return data["ahead_by"]
    return -1


def get_owner() -> str:
    result = subprocess.run(
        ["gh", "repo", "view", "--json", "owner", "--jq", ".owner.login"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def fetch_repos(owner: str) -> list[dict]:
    """Fetch all repos with branch info via GraphQL, handling pagination and org/user."""
    for account_type in ("organization", "user"):
        query = GRAPHQL_QUERY % account_type
        repos = []
        cursor = None

        while True:
            variables = {"owner": owner}
            if cursor:
                variables["cursor"] = cursor

            data = gh_graphql(query, variables)
            account = data.get("data", {}).get(account_type)
            if not account:
                break

            page = account["repositories"]
            repos.extend(page["nodes"])

            if page["pageInfo"]["hasNextPage"]:
                cursor = page["pageInfo"]["endCursor"]
            else:
                break

        if repos:
            return repos

    return []


def main():
    owner = get_owner()
    if not owner:
        print("Error: could not determine repo owner. Is gh authenticated?", file=sys.stderr)
        sys.exit(1)

    # Pre-fetch token once before threading
    get_token()

    repos = fetch_repos(owner)
    if not repos:
        print(f"No repositories found for **{owner}**.")
        sys.exit(0)

    # Build list of comparisons to make
    comparisons = []  # (repo_name, base, head, category, extra)

    for repo in repos:
        name = repo["name"]
        default_ref = repo.get("defaultBranchRef")
        if not default_ref:
            continue
        default_branch = default_ref["name"]
        has_develop = repo.get("develop") is not None
        has_uat = repo.get("uatMain") is not None
        release_nodes = repo.get("releaseBranches", {}).get("nodes") or []

        if has_develop:
            comparisons.append((name, "develop", default_branch, "main_ahead_develop", default_branch))

        for rb in release_nodes:
            rb_name = f"release/{rb['name']}"
            comparisons.append((name, default_branch, rb_name, "release_ahead_main", None))

        if has_develop and has_uat:
            comparisons.append((name, "UAT/main", "develop", "develop_ahead_uat", None))

    main_ahead_develop = []
    release_ahead_main = []
    develop_ahead_uat = []

    def run_compare(comp):
        repo_name, base, head, category, extra = comp
        n = ahead_by(owner, repo_name, base, head)
        return (repo_name, base, head, category, extra, n)

    with ThreadPoolExecutor(max_workers=20) as pool:
        futures = [pool.submit(run_compare, c) for c in comparisons]
        for future in as_completed(futures):
            repo_name, base, head, category, extra, n = future.result()
            if n > 0:
                if category == "main_ahead_develop":
                    main_ahead_develop.append((repo_name, extra, n))
                elif category == "release_ahead_main":
                    release_ahead_main.append((repo_name, head, n))
                elif category == "develop_ahead_uat":
                    develop_ahead_uat.append((repo_name, n))

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
