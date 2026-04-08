#!/usr/bin/env python3
"""Check Claude usage/quota by parsing the settings page HTML.

Usage:
    python usage_check.py <html_file>

Reads the HTML content from a file (piped from WebFetch or saved),
extracts usage percentage and reset time, and outputs a formatted
summary box.

If parsing fails, outputs the raw text (truncated) for debugging.
"""

import re
import sys
from datetime import datetime, timezone


BAR_WIDTH = 28


def extract_usage_percentage(text: str) -> int | None:
    """Try various patterns to find a usage percentage."""
    # "42% used" or "42%" near usage context
    m = re.search(r"(\d{1,3})\s*%\s*(?:used|of)", text, re.IGNORECASE)
    if m:
        return int(m.group(1))

    # "58% remaining" → invert
    m = re.search(r"(\d{1,3})\s*%\s*remaining", text, re.IGNORECASE)
    if m:
        return 100 - int(m.group(1))

    # Progress bar value attributes
    m = re.search(r'(?:value|aria-valuenow)\s*=\s*["\']?(\d{1,3})', text, re.IGNORECASE)
    if m:
        return int(m.group(1))

    # Fraction like "420 / 1000" near usage
    m = re.search(r"(\d+(?:,\d+)?)\s*/\s*(\d+(?:,\d+)?)", text)
    if m:
        num = int(m.group(1).replace(",", ""))
        den = int(m.group(2).replace(",", ""))
        if den > 0:
            return round(num / den * 100)

    # Bare percentage near "usage" or "limit"
    m = re.search(r"(?:usage|limit|quota).*?(\d{1,3})\s*%", text, re.IGNORECASE)
    if m:
        return int(m.group(1))

    return None


def extract_reset_time(text: str) -> str | None:
    """Try various patterns to find the reset time."""
    # "Resets in Xh Ym" or "resets in X hours"
    m = re.search(r"resets?\s+in\s+([\dhm\s]+(?:hours?|minutes?|hrs?|mins?)?[\dhm\s]*)", text, re.IGNORECASE)
    if m:
        return m.group(1).strip()

    # "Next reset: <time>"
    m = re.search(r"next\s+reset[:\s]+(.+?)(?:\n|$)", text, re.IGNORECASE)
    if m:
        return m.group(1).strip()

    # ISO datetime
    m = re.search(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2}))", text)
    if m:
        try:
            dt = datetime.fromisoformat(m.group(1))
            now = datetime.now(timezone.utc)
            delta = dt - now
            if delta.total_seconds() > 0:
                hours = int(delta.total_seconds() // 3600)
                minutes = int((delta.total_seconds() % 3600) // 60)
                return f"in {hours}h {minutes:02d}m"
        except ValueError:
            return m.group(1)

    # Relative like "3 hours" near reset
    m = re.search(r"(\d+)\s*(hours?|minutes?|hrs?|mins?)\s*(?:until|before|left)", text, re.IGNORECASE)
    if m:
        return f"in {m.group(1)} {m.group(2)}"

    return None


def render_box(pct: int | None, reset: str | None, raw_text: str) -> str:
    lines = []
    lines.append("┌─ Claude Usage ─────────────────────────────┐")

    if pct is not None:
        remaining = 100 - pct
        filled = round(BAR_WIDTH * pct / 100)
        empty = BAR_WIDTH - filled
        bar = "█" * filled + "░" * empty

        lines.append(f"│ Used:       {pct}%{' ' * (33 - len(str(pct)))}│")
        lines.append(f"│ Remaining:  {remaining}%{' ' * (33 - len(str(remaining)))}│")
        lines.append(f"│{' ' * 46}│")
        bar_line = f" {bar}  {pct}%"
        lines.append(f"│{bar_line}{' ' * (46 - len(bar_line))}│")
        lines.append(f"│{' ' * 46}│")
    else:
        lines.append(f"│ Usage percentage: not found{' ' * 19}│")
        lines.append(f"│{' ' * 46}│")

    if reset is not None:
        reset_line = f" Next reset: {reset}"
        padding = 46 - len(reset_line)
        if padding < 0:
            reset_line = reset_line[:46]
            padding = 0
        lines.append(f"│{reset_line}{' ' * padding}│")
    else:
        lines.append(f"│ Next reset: not found{' ' * 25}│")

    lines.append("└──────────────────────────────────────────────┘")

    if pct is None and reset is None:
        lines.append("\nRaw page content (truncated):")
        lines.append(raw_text[:500])

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python usage_check.py <html_file>")
        print("  Pass '-' to read from stdin")
        sys.exit(1)

    source = sys.argv[1]
    if source == "-":
        text = sys.stdin.read()
    else:
        with open(source, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()

    pct = extract_usage_percentage(text)
    reset = extract_reset_time(text)
    output = render_box(pct, reset, text)
    sys.stdout.buffer.write(output.encode("utf-8"))
    sys.stdout.buffer.write(b"\n")


if __name__ == "__main__":
    main()
