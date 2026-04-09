#!/usr/bin/env python3
"""Analyse git history to estimate time spent on a project.

Usage:
    python estimate_time.py                        # all commits
    python estimate_time.py "3 months"             # relative period
    python estimate_time.py 2026-03-01             # since date
    python estimate_time.py 2026-03-01 2026-03-14  # date range

Output: a Markdown-formatted summary table with per-contributor
session breakdowns and totals.
"""

import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta

SESSION_GAP_HOURS = 2
SETUP_MINUTES = 30
SOLO_COMMIT_MINUTES = 37  # midpoint of 30-45


def parse_args(args: list[str]) -> tuple[str | None, str | None]:
    """Return (after_date, before_date) from CLI arguments."""
    if not args:
        return None, None

    # Two explicit dates
    if len(args) >= 2:
        return args[0], args[1]

    arg = " ".join(args)

    # Single ISO date
    try:
        datetime.strptime(arg, "%Y-%m-%d")
        return arg, None
    except ValueError:
        pass

    # Relative period like "3 months", "2 weeks", "30 days", "1 year"
    parts = arg.lower().split()
    if len(parts) == 2:
        try:
            n = int(parts[0])
        except ValueError:
            print(f"Error: cannot parse argument '{arg}'", file=sys.stderr)
            sys.exit(1)

        unit = parts[1].rstrip("s")  # normalise plural
        now = datetime.now()
        if unit == "day":
            start = now - timedelta(days=n)
        elif unit == "week":
            start = now - timedelta(weeks=n)
        elif unit == "month":
            start = now - timedelta(days=n * 30)
        elif unit == "year":
            start = now - timedelta(days=n * 365)
        else:
            print(f"Error: unknown unit '{parts[1]}'", file=sys.stderr)
            sys.exit(1)
        return start.strftime("%Y-%m-%d"), None

    print(f"Error: cannot parse argument '{arg}'", file=sys.stderr)
    sys.exit(1)


def get_git_log(after: str | None, before: str | None) -> str:
    cmd = ["git", "log", "--format=%ai\t%ae\t%an\t%s", "--all"]
    if after:
        cmd.append(f"--after={after}")
    if before:
        cmd.append(f"--before={before}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running git log: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def parse_log(raw: str) -> list[dict]:
    commits = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t", 3)
        if len(parts) < 4:
            continue
        dt_str, email, name, subject = parts
        # git date format: 2026-03-14 10:23:45 +0000
        dt = datetime.strptime(dt_str[:19], "%Y-%m-%d %H:%M:%S")
        commits.append({
            "dt": dt,
            "email": email,
            "name": name,
            "subject": subject,
        })
    return commits


def group_sessions(commits: list[dict]) -> list[list[dict]]:
    """Group commits into sessions (<=2h gap)."""
    if not commits:
        return []
    sorted_commits = sorted(commits, key=lambda c: c["dt"])
    sessions = [[sorted_commits[0]]]
    for c in sorted_commits[1:]:
        gap = (c["dt"] - sessions[-1][-1]["dt"]).total_seconds() / 3600
        if gap <= SESSION_GAP_HOURS:
            sessions[-1].append(c)
        else:
            sessions.append([c])
    return sessions


def estimate_session_hours(session: list[dict]) -> float:
    if len(session) == 1:
        return SOLO_COMMIT_MINUTES / 60
    first = session[0]["dt"]
    last = session[-1]["dt"]
    span_min = (last - first).total_seconds() / 60
    return (span_min + SETUP_MINUTES) / 60


def format_duration(hours: float) -> str:
    h = int(hours)
    m = int((hours - h) * 60)
    if h == 0:
        return f"{m}m"
    return f"{h}h {m:02d}m"


def main():
    after, before = parse_args(sys.argv[1:])
    raw = get_git_log(after, before)

    if not raw:
        print("No commits found in the specified range.")
        sys.exit(0)

    commits = parse_log(raw)
    if not commits:
        print("No commits found in the specified range.")
        sys.exit(0)

    # Group by contributor
    by_author: dict[str, list[dict]] = defaultdict(list)
    for c in commits:
        by_author[c["name"]].append(c)

    date_range = sorted(c["dt"] for c in commits)
    range_start = date_range[0].strftime("%Y-%m-%d")
    range_end = date_range[-1].strftime("%Y-%m-%d")

    print(f"## Time Estimate: {range_start} to {range_end}")
    print(f"**{len(commits)} commits** across **{len(by_author)} contributor(s)**\n")

    overall_hours = 0.0
    summary_rows = []

    for author in sorted(by_author.keys()):
        author_commits = by_author[author]
        sessions = group_sessions(author_commits)
        author_hours = 0.0

        print(f"### {author}")
        print(f"| # | Date | Commits | Duration | First commit |")
        print(f"|---|------|---------|----------|--------------|")

        for i, session in enumerate(sessions, 1):
            s_date = session[0]["dt"].strftime("%Y-%m-%d")
            s_hours = estimate_session_hours(session)
            author_hours += s_hours
            first_subject = session[0]["subject"]
            if len(first_subject) > 50:
                first_subject = first_subject[:47] + "..."
            print(f"| {i} | {s_date} | {len(session)} | {format_duration(s_hours)} | {first_subject} |")

        print(f"\n**{author} total: {format_duration(author_hours)}** ({len(sessions)} sessions, {len(author_commits)} commits)\n")
        summary_rows.append((author, author_hours, len(sessions), len(author_commits)))
        overall_hours += author_hours

    # Summary table
    if len(summary_rows) > 1:
        print("### Summary")
        print("| Contributor | Hours | Sessions | Commits |")
        print("|-------------|-------|----------|---------|")
        for name, hours, sessions, commit_count in summary_rows:
            print(f"| {name} | {format_duration(hours)} | {sessions} | {commit_count} |")
        print(f"| **Total** | **{format_duration(overall_hours)}** | **{sum(r[2] for r in summary_rows)}** | **{sum(r[3] for r in summary_rows)}** |")

    if len(summary_rows) == 1:
        print(f"### Total: {format_duration(overall_hours)}")

    # Caveats
    print("\n---")
    print("*Caveats: session grouping uses a 2h gap threshold + 30min setup overhead. "
          "Single commits estimated at ~37min. Merge commits, rebases, and "
          "timezone differences may skew results.*")


if __name__ == "__main__":
    main()
