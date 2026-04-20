#!/usr/bin/env python3
"""Copy text to the OS clipboard.

Reusable helper for skills that want to hand the user a paste-ready value
instead of asking them to retype it. The copied value also flows into the
OS clipboard history panel (Win+V on Windows, if history is enabled).

Usage:
    python copy_to_clipboard.py "value to copy"   # argv
    echo "value to copy" | python copy_to_clipboard.py   # stdin

Exactly one source is required. On success, exits 0 and prints nothing.
On failure, prints a reason to stderr and exits non-zero so callers can
decide how to report the error.

Platform support:
  - Windows: PowerShell `Set-Clipboard`. The value is passed via an env
    var (`CLAUDE_CLIP_VALUE`) so callers don't have to escape quotes,
    newlines, dollar signs, or backticks.
  - macOS:   `pbcopy`.
  - Linux:   first available of `wl-copy` (Wayland), `xclip`, `xsel`.
"""
import os
import subprocess
import sys


def copy_windows(text: str) -> None:
    env = os.environ.copy()
    env["CLAUDE_CLIP_VALUE"] = text
    subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            "Set-Clipboard -Value $env:CLAUDE_CLIP_VALUE",
        ],
        env=env,
        check=True,
    )


def copy_macos(text: str) -> None:
    subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)


def copy_linux(text: str) -> None:
    candidates = [
        ["wl-copy"],
        ["xclip", "-selection", "clipboard"],
        ["xsel", "--clipboard", "--input"],
    ]
    data = text.encode("utf-8")
    last_err = None
    for cmd in candidates:
        try:
            subprocess.run(cmd, input=data, check=True)
            return
        except FileNotFoundError as e:
            last_err = e
            continue
    raise RuntimeError(
        "no clipboard tool available (install wl-clipboard, xclip, or xsel)"
    ) from last_err


def main() -> int:
    if len(sys.argv) > 2:
        print("usage: copy_to_clipboard.py [value]", file=sys.stderr)
        return 2

    if len(sys.argv) == 2:
        text = sys.argv[1]
    elif not sys.stdin.isatty():
        # Force UTF-8 on stdin: on Windows the default is the console
        # code page (e.g. cp1252), which corrupts multi-byte characters
        # like emoji when callers pipe them in via `printf ... |`.
        text = sys.stdin.buffer.read().decode("utf-8", errors="replace")
    else:
        print("ERROR: no value given (pass as argv or pipe via stdin)", file=sys.stderr)
        return 2

    try:
        if sys.platform.startswith("win"):
            copy_windows(text)
        elif sys.platform == "darwin":
            copy_macos(text)
        else:
            copy_linux(text)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: clipboard tool failed (exit {e.returncode})", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"ERROR: clipboard tool not found: {e}", file=sys.stderr)
        return 1
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
