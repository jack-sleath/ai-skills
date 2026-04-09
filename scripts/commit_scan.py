#!/usr/bin/env python3
"""Pre-commit scanner: checks diff for encoding corruption and secrets.

Usage:
    python commit_scan.py

Exits 0 if clean, 1 if issues found. Output is Markdown-formatted.
Also reports which skill files in commands/ were added/removed/renamed
so the caller can check README.md and SKILL-GRAPH.md.
"""

import re
import subprocess
import sys


# Mojibake sequences that indicate encoding corruption
MOJIBAKE_PATTERNS = [
    r"Ã¢â‚¬[\"â„¢\x9c\x9d\x93\x94]",
    r"Ã‚Â",
    r"ÃƒÂ",
    r"Ã©",
    r"Ã¨",
    r"Ã¼",
    r"Ã¶",
    r"Ã¤",
    r"â€[\"™\x9c\x9d\x93\x94]",
    r"Â[\xa0-\xff]",
]

# Secret patterns: KEY=<long_value>, token/password assignments, private keys
SECRET_PATTERNS = [
    (r"(?:API[_-]?KEY|SECRET[_-]?KEY|ACCESS[_-]?KEY|PRIVATE[_-]?KEY)\s*[=:]\s*['\"]?[A-Za-z0-9/+=_-]{20,}", "API/secret key assignment"),
    (r"(?:TOKEN|AUTH[_-]?TOKEN|BEARER)\s*[=:]\s*['\"]?[A-Za-z0-9/+=_.-]{20,}", "Token assignment"),
    (r"(?:PASSWORD|PASSWD|DB_PASS)\s*[=:]\s*['\"]?.{8,}", "Password assignment"),
    (r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----", "Private key"),
    (r"(?:sk-[a-zA-Z0-9]{20,})", "OpenAI/Anthropic API key"),
    (r"(?:ghp_[a-zA-Z0-9]{36,})", "GitHub personal access token"),
    (r"(?:AKIA[0-9A-Z]{16})", "AWS access key ID"),
]


def get_diff() -> str:
    result = subprocess.run(
        ["git", "diff", "HEAD"],
        capture_output=True, text=True, errors="replace",
    )
    return result.stdout


def get_status() -> str:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True,
    )
    return result.stdout


def scan_mojibake(diff: str) -> list[dict]:
    issues = []
    current_file = None
    for line in diff.splitlines():
        if line.startswith("diff --git"):
            m = re.search(r"b/(.+)$", line)
            current_file = m.group(1) if m else "unknown"
        elif line.startswith("+") and not line.startswith("+++"):
            for pattern in MOJIBAKE_PATTERNS:
                if re.search(pattern, line):
                    issues.append({
                        "file": current_file,
                        "line": line[1:].strip()[:80],
                        "type": "mojibake",
                    })
                    break
    return issues


def scan_secrets(diff: str) -> list[dict]:
    issues = []
    current_file = None
    for line in diff.splitlines():
        if line.startswith("diff --git"):
            m = re.search(r"b/(.+)$", line)
            current_file = m.group(1) if m else "unknown"
        elif line.startswith("+") and not line.startswith("+++"):
            # Skip .md files and comments — high false-positive rate
            if current_file and current_file.endswith(".md"):
                continue
            for pattern, label in SECRET_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append({
                        "file": current_file,
                        "line": line[1:].strip()[:80],
                        "type": label,
                    })
                    break
    return issues


def detect_skill_changes(status: str) -> list[str]:
    """Find added/deleted/renamed files in commands/."""
    changes = []
    for line in status.splitlines():
        line = line.strip()
        if not line:
            continue
        code = line[:2].strip()
        path = line[3:].strip().strip('"')
        if "commands/" in path and path.endswith(".md"):
            if code in ("A", "?", "??"):
                changes.append(f"added: {path}")
            elif code == "D":
                changes.append(f"deleted: {path}")
            elif code.startswith("R"):
                changes.append(f"renamed: {path}")
            elif code == "M":
                changes.append(f"modified: {path}")
    return changes


def main():
    status = get_status()
    if not status.strip():
        print("nothing to commit")
        sys.exit(0)

    diff = get_diff()
    if not diff.strip():
        # Only untracked files, no diff to scan
        print("## Scan: OK (untracked files only, no diff to scan)")

    mojibake = scan_mojibake(diff)
    secrets = scan_secrets(diff)
    skill_changes = detect_skill_changes(status)

    has_issues = bool(mojibake or secrets)

    if has_issues:
        print("## Scan: BLOCKED\n")

    if mojibake:
        print("### Encoding corruption detected\n")
        for issue in mojibake:
            print(f"- **{issue['file']}**: `{issue['line']}`")
        print()

    if secrets:
        print("### Potential secrets detected\n")
        for issue in secrets:
            print(f"- **{issue['file']}** ({issue['type']}): `{issue['line']}`")
        print()

    if not has_issues:
        print("## Scan: OK\n")

    if skill_changes:
        print("### Skill file changes detected\n")
        for change in skill_changes:
            print(f"- {change}")
        print("\nVerify that `README.md` and `SKILL-GRAPH.md` are updated.")

    sys.exit(1 if has_issues else 0)


if __name__ == "__main__":
    main()
