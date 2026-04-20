#!/usr/bin/env python3
"""
Eval runner for ai-skills commands.

Runs a command against test fixtures, scores the output against criteria,
and optionally loops to evolve the command prompt.

Uses the Claude Code CLI (`claude -p`) instead of the Anthropic API directly,
so no API key is needed — just a working `claude` installation.

Usage:
    python evals/run.py feature                           # single eval run
    python evals/run.py feature --evolve --runs 3         # evolve for score (default)
    python evals/run.py feature --evolve --optimize tokens # evolve to reduce token usage
    python evals/run.py feature --evolve --optimize both   # improve score + reduce tokens
    python evals/run.py feature --optimize tokens --min-score 20  # keep score >= 20
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

EVALS_DIR = Path(__file__).resolve().parent
ROOT_DIR = EVALS_DIR.parent
COMMANDS_DIR = ROOT_DIR / "commands"
CRITERIA_DIR = EVALS_DIR / "criteria"
FIXTURES_DIR = EVALS_DIR / "fixtures"
RESULTS_DIR = EVALS_DIR / "results"

DEFAULT_MODEL = "claude-sonnet-4-6"


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_fixtures(command_name: str) -> dict[str, str]:
    """Load all fixture files for a command into a dict of {filename: content}."""
    fixture_dir = FIXTURES_DIR / command_name
    if not fixture_dir.is_dir():
        sys.exit(f"No fixtures found at {fixture_dir}")
    return {f.name: read_file(f) for f in sorted(fixture_dir.iterdir()) if f.is_file()}


def build_execution_prompt(command_content: str, fixtures: dict[str, str]) -> str:
    """Build the prompt that simulates running the command against fixtures."""
    fixture_block = "\n\n".join(
        f"### {name}\n```\n{content}\n```" for name, content in fixtures.items()
    )
    return (
        "You are Claude Code executing a skill command. The skill instructions and "
        "the project files are provided below.\n\n"
        "IMPORTANT: This is a non-interactive evaluation run. You cannot ask the user "
        "questions. For any fields that would normally require user input, use a clear "
        'placeholder like "[To be confirmed]" or "[TBC]".\n\n'
        "Execute the skill and produce ONLY the output document — no preamble, no "
        "explanation, just the document content.\n\n"
        "## Skill Instructions\n\n"
        f"{command_content}\n\n"
        "## Project Files\n\n"
        f"{fixture_block}"
    )


def build_scoring_prompt(criteria_content: str, command_output: str) -> str:
    """Build the prompt for scoring the command output."""
    return (
        "You are an evaluator. Score the following command output against the "
        "criteria below.\n\n"
        "## Evaluation Criteria\n\n"
        f"{criteria_content}\n\n"
        "## Command Output to Score\n\n"
        f"```\n{command_output}\n```"
    )


def load_related_scripts(command_name: str) -> dict[str, str]:
    """Load any Python helper scripts that the skill references.

    Checks scripts/ for files matching the command name or mentioned in the
    skill file content.
    """
    scripts_dir = ROOT_DIR / "scripts"
    if not scripts_dir.is_dir():
        return {}

    command_path = COMMANDS_DIR / f"{command_name}.md"
    skill_text = read_file(command_path) if command_path.exists() else ""

    result: dict[str, str] = {}
    for f in sorted(scripts_dir.iterdir()):
        if not f.is_file() or f.suffix != ".py":
            continue
        # Include scripts that share the command name or are referenced in the skill
        if command_name.replace("-", "_") in f.stem or f"scripts/{f.name}" in skill_text:
            result[f"scripts/{f.name}"] = read_file(f)
    return result


def build_evolution_prompt(
    command_content: str,
    scores: dict,
    command_output: str,
    criteria_content: str = "",
    existing_scripts: dict[str, str] | None = None,
    optimize: str = "score",
    token_usage: dict | None = None,
    min_score: int | None = None,
) -> str:
    """Build the prompt for evolving the command based on scores and optimization target."""
    if optimize == "tokens":
        objective = (
            "Your task: Edit the skill definition to REDUCE TOKEN USAGE while "
            f"keeping the total score at or above {min_score}. "
            "Strategies:\n"
            "- Remove redundant instructions, combine similar steps, use concise phrasing\n"
            "- Eliminate unnecessary examples and reduce output verbosity requirements\n"
            "- Offload expensive work to local Python scripts in `scripts/` that the "
            "skill calls via Bash — e.g. parsing, formatting, data extraction, "
            "validation. These run offline with zero token cost. The skill should "
            "call them with `python scripts/<name>.py` and use their output.\n"
            "- If you create a helper script, include its full content in a new "
            "section at the end of your response, fenced as:\n"
            "  SCRIPT: scripts/<name>.py\n"
            "  ```python\n  ...code...\n  ```\n"
            "Do NOT sacrifice quality — only cut waste.\n\n"
        )
    elif optimize == "both":
        objective = (
            "Your task: Edit the skill definition to BOTH improve scores AND "
            "reduce token usage. Prioritise fixing the lowest-scoring dimensions "
            "first, but also look for opportunities to tighten the prompt — remove "
            "redundancy, combine steps, use concise phrasing. Every token saved "
            "without losing quality is a win.\n\n"
            "You can also offload expensive work to local Python scripts in "
            "`scripts/` — e.g. parsing, formatting, data extraction — which run "
            "offline with zero token cost. If you create a helper script, include "
            "its full content fenced as:\n"
            "  SCRIPT: scripts/<name>.py\n"
            "  ```python\n  ...code...\n  ```\n\n"
        )
    else:  # score (default)
        objective = (
            "Your task: Edit the skill definition to improve the lowest-scoring "
            "dimensions. Make targeted, minimal changes — do not rewrite from scratch. "
            "Preserve the overall structure and intent of the skill.\n\n"
            "If the skill calls a Python helper script in `scripts/`, you may also "
            "modify that script to improve the output quality. If creating or "
            "modifying a script would help score higher (e.g. better formatting, "
            "richer data extraction), include its full content fenced as:\n"
            "  SCRIPT: scripts/<name>.py\n"
            "  ```python\n  ...code...\n  ```\n\n"
        )

    token_block = ""
    if token_usage and optimize in ("tokens", "both"):
        exec_usage = token_usage.get("execution", {})
        token_block = (
            "## Token Usage\n\n"
            f"- Execution input tokens: {exec_usage.get('input_tokens', '?'):,}\n"
            f"- Execution output tokens: {exec_usage.get('output_tokens', '?'):,}\n"
            f"- Execution total tokens: {exec_usage.get('total_tokens', '?'):,}\n\n"
            "Aim to reduce these numbers in the next iteration.\n\n"
        )

    criteria_block = ""
    if criteria_content:
        criteria_block = (
            "## Evaluation Criteria\n\n"
            "This is the rubric used to score the output. Study the dimension "
            "descriptions and score anchors to understand exactly what the "
            "evaluator rewards and penalises.\n\n"
            f"{criteria_content}\n\n"
        )

    scripts_block = ""
    if existing_scripts:
        parts = []
        for path, content in existing_scripts.items():
            parts.append(f"### {path}\n```python\n{content}\n```")
        scripts_block = (
            "## Existing Helper Scripts\n\n"
            "The skill currently uses these Python scripts. You may modify them "
            "to improve output quality or efficiency. Include any changed script "
            "in a SCRIPT: block at the end of your response.\n\n"
            + "\n\n".join(parts) + "\n\n"
        )

    return (
        "You are an expert prompt engineer improving a Claude Code skill command.\n\n"
        "Below is the current skill definition, the output it produced, the "
        "evaluation criteria, and the scores with suggestions.\n\n"
        f"{objective}"
        "Return ONLY the improved skill file content — no explanation, no markdown "
        "fences, just the raw .md content.\n\n"
        "## Current Skill Definition\n\n"
        f"{command_content}\n\n"
        f"{scripts_block}"
        "## Output Produced\n\n"
        f"```\n{command_output}\n```\n\n"
        f"{criteria_block}"
        "## Evaluation Scores\n\n"
        f"```json\n{json.dumps(scores, indent=2)}\n```\n\n"
        f"{token_block}"
    )


def call_claude(prompt: str, model: str) -> tuple[str, dict]:
    """Call the Claude CLI and return (response_text, usage_dict)."""
    result = subprocess.run(
        [
            "claude", "-p",
            "--output-format", "json",
            "--model", model,
        ],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=300,
    )
    if result.returncode != 0:
        sys.exit(
            f"Claude CLI failed (exit {result.returncode}):\n"
            f"stderr: {result.stderr}\n"
            f"stdout: {result.stdout[:500]}"
        )

    data = json.loads(result.stdout)

    # Check for CLI-level errors (e.g. not logged in)
    if data.get("is_error"):
        sys.exit(f"Claude CLI error: {data.get('result', 'unknown error')}")

    text = data.get("result", "")

    # Extract token usage from the CLI JSON response
    cli_usage = data.get("usage", {})
    input_tokens = cli_usage.get("input_tokens", 0)
    output_tokens = cli_usage.get("output_tokens", 0)
    usage = {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "cost_usd": data.get("total_cost_usd", 0),
    }
    return text, usage


def parse_scores(raw: str) -> dict:
    """Extract JSON scores from the evaluator response."""
    # Find JSON block — it may be wrapped in ```json ... ```
    text = raw.strip()
    if "```" in text:
        start = text.find("{")
        end = text.rfind("}") + 1
        text = text[start:end]
    return json.loads(text)


def extract_scripts(content: str) -> tuple[str, dict[str, str]]:
    """Extract helper scripts from evolution output.

    Looks for blocks like:
        SCRIPT: scripts/foo.py
        ```python
        ...code...
        ```

    Returns (cleaned_content, {path: code}) with script blocks removed.
    """
    scripts: dict[str, str] = {}
    # Match SCRIPT: path followed by a fenced code block
    pattern = re.compile(
        r'\n*SCRIPT:\s*(scripts/\S+)\s*\n'
        r'```(?:python)?\s*\n'
        r'(.*?)'
        r'\n```',
        re.DOTALL,
    )
    for m in pattern.finditer(content):
        scripts[m.group(1)] = m.group(2)
    cleaned = pattern.sub('', content).rstrip() + '\n'
    return cleaned, scripts


def save_result(command_name: str, iteration: int, result: dict) -> Path:
    """Save a single iteration result to the results directory."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"{command_name}_iter{iteration}_{timestamp}.json"
    out_path = RESULTS_DIR / filename
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return out_path


def run_single_eval(command_name: str, model: str) -> dict:
    """Run one eval cycle: execute command -> score output. Returns result dict."""
    command_path = COMMANDS_DIR / f"{command_name}.md"
    criteria_path = CRITERIA_DIR / f"{command_name}.md"

    if not command_path.exists():
        sys.exit(f"Command not found: {command_path}")
    if not criteria_path.exists():
        sys.exit(f"Criteria not found: {criteria_path}")

    command_content = read_file(command_path)
    criteria_content = read_file(criteria_path)
    fixtures = load_fixtures(command_name)

    # Step 1: Execute the command
    print("  Running command...", flush=True)
    exec_prompt = build_execution_prompt(command_content, fixtures)
    command_output, exec_usage = call_claude(exec_prompt, model)

    # Step 2: Score the output
    print("  Scoring output...", flush=True)
    score_prompt = build_scoring_prompt(criteria_content, command_output)
    score_raw, score_usage = call_claude(score_prompt, model)
    try:
        scores = parse_scores(score_raw)
    except (json.JSONDecodeError, ValueError):
        print("  Score parse failed, retrying...", flush=True)
        repair_prompt = (
            "The following text was supposed to be a valid JSON object but could "
            "not be parsed. Return ONLY the corrected JSON object:\n\n"
            f"{score_raw}"
        )
        score_raw2, retry_usage = call_claude(repair_prompt, model)
        score_usage = {
            k: score_usage[k] + retry_usage[k]
            for k in ("input_tokens", "output_tokens", "total_tokens")
        }
        score_usage["cost_usd"] = (
            score_usage.get("cost_usd", 0) + retry_usage.get("cost_usd", 0)
        )
        scores = parse_scores(score_raw2)

    total_usage = {
        "execution": exec_usage,
        "scoring": score_usage,
        "combined": {
            "input_tokens": exec_usage["input_tokens"] + score_usage["input_tokens"],
            "output_tokens": exec_usage["output_tokens"] + score_usage["output_tokens"],
            "total_tokens": exec_usage["total_tokens"] + score_usage["total_tokens"],
            "cost_usd": exec_usage.get("cost_usd", 0) + score_usage.get("cost_usd", 0),
        },
    }

    return {
        "command": command_name,
        "model": model,
        "command_content": command_content,
        "command_output": command_output,
        "scores": scores,
        "token_usage": total_usage,
    }


def evolve_command(
    command_name: str,
    command_output: str,
    scores: dict,
    model: str,
    criteria_content: str = "",
    optimize: str = "score",
    token_usage: dict | None = None,
    min_score: int | None = None,
) -> tuple[str, dict]:
    """Use the CLI to improve the command based on scores. Returns (new_content, usage)."""
    command_path = COMMANDS_DIR / f"{command_name}.md"
    command_content = read_file(command_path)

    existing_scripts = load_related_scripts(command_name)

    print("  Evolving command...", flush=True)
    evolve_prompt = build_evolution_prompt(
        command_content, scores, command_output,
        criteria_content=criteria_content,
        existing_scripts=existing_scripts,
        optimize=optimize, token_usage=token_usage, min_score=min_score,
    )
    new_content, usage = call_claude(evolve_prompt, model)
    return new_content, usage


def print_scores(scores: dict) -> None:
    """Pretty-print the score breakdown."""
    dims = {k: v for k, v in scores.items() if isinstance(v, dict) and "score" in v}
    num_dims = len(dims) or 1
    max_per = scores.get("max_possible", num_dims * 10) // num_dims
    for key, val in dims.items():
        print(f"    {key}: {val['score']}/{max_per} — {val.get('reasoning', '')}")
    print(f"    TOTAL: {scores.get('total', '?')}/{scores.get('max_possible', '?')}")
    suggestions = scores.get("suggestions", [])
    if suggestions:
        print("    Suggestions:")
        for s in suggestions:
            print(f"      - {s}")


def print_usage(usage: dict) -> None:
    """Pretty-print token usage."""
    combined = usage.get("combined", usage)
    cost = combined.get("cost_usd", 0)
    cost_str = f"  cost: ${cost:.4f}" if cost else ""
    print(
        f"    Tokens — in: {combined['input_tokens']:,}  "
        f"out: {combined['output_tokens']:,}  "
        f"total: {combined['total_tokens']:,}"
        f"{cost_str}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Eval runner for ai-skills commands")
    parser.add_argument("command", help="Command name (e.g. 'feature')")
    parser.add_argument(
        "--evolve", action="store_true", help="Enable evolution loop"
    )
    parser.add_argument(
        "--runs", type=int, default=3, help="Number of evolution iterations (default: 3)"
    )
    parser.add_argument(
        "--model", default=DEFAULT_MODEL, help=f"Model to use (default: {DEFAULT_MODEL})"
    )
    parser.add_argument(
        "--optimize",
        choices=["score", "tokens", "both"],
        default="score",
        help="Optimization target: score (default), tokens, or both",
    )
    parser.add_argument(
        "--min-score",
        type=int,
        default=None,
        help="Minimum total score to maintain when --optimize is tokens or both",
    )
    parser.add_argument(
        "--score",
        type=float,
        default=None,
        help="Stop early when score reaches this percentage (e.g. 85)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print prompts without calling the CLI"
    )
    args = parser.parse_args()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    SCRIPTS_DIR = ROOT_DIR / "scripts"

    # Load criteria once for the evolution prompt
    criteria_path = CRITERIA_DIR / f"{args.command}.md"
    criteria_content = read_file(criteria_path) if criteria_path.exists() else ""

    command_path = COMMANDS_DIR / f"{args.command}.md"
    original_content = read_file(command_path)

    all_results = []
    best_score = 0
    best_content = original_content
    best_iter = 0

    # Phase tracking for --optimize both
    phase = 1
    current_optimize = "score" if args.optimize == "both" else args.optimize
    min_score = args.min_score

    if args.optimize == "both":
        print("\n  -- Phase 1: Score optimisation --")

    for i in range(1, args.runs + 1 if args.evolve else 2):
        print(f"\n{'='*60}")
        print(f"  Iteration {i}" + (f" of {args.runs}" if args.evolve else ""))
        print(f"{'='*60}")

        if args.dry_run:
            fixtures = load_fixtures(args.command)
            command_content = read_file(command_path)
            print("\n[DRY RUN] Execution prompt length:",
                  len(build_execution_prompt(command_content, fixtures)), "chars")
            break

        result = run_single_eval(args.command, args.model)
        result["iteration"] = i

        print("\n  Scores:")
        print_scores(result["scores"])
        print("\n  Token Usage:")
        print_usage(result["token_usage"])

        current_total = result["scores"].get("total", 0)
        max_possible = result["scores"].get("max_possible", 0)

        # Save result
        out_path = save_result(args.command, i, result)
        print(f"\n  Result saved to {out_path.name}")
        all_results.append(result)

        # -- Best-version tracking --
        if current_total > best_score:
            best_score = current_total
            best_content = read_file(command_path)
            best_iter = i
        elif current_total < best_score and args.evolve:
            # Revert to best before next evolution so we don't build on a regression
            command_path.write_text(best_content, encoding="utf-8")
            print(f"  Score regressed — reverted to iteration {best_iter} (score {best_score})")

        # -- Early stop: --score threshold --
        if args.score is not None and max_possible > 0:
            pct = current_total / max_possible * 100
            if pct >= args.score:
                if args.optimize == "both" and phase == 1:
                    # Switch to phase 2 instead of stopping
                    phase = 2
                    current_optimize = "tokens"
                    if min_score is None:
                        min_score = best_score
                    print(f"\n  -- Phase 2: Token optimisation (score floor: {min_score}) --")
                else:
                    print(f"\n  Score threshold reached ({pct:.0f}% >= {args.score:.0f}%) — stopping.")
                    break

        # -- Early stop: perfect score --
        if current_optimize == "score" and max_possible > 0 and current_total >= max_possible:
            if args.optimize == "both":
                phase = 2
                current_optimize = "tokens"
                if min_score is None:
                    min_score = best_score
                print(f"\n  Perfect score — switching to token optimisation (floor: {min_score})")
            else:
                print("\n  Perfect score — stopping early.")
                break

        # -- Early stop: negligible token change in token phase --
        if current_optimize == "tokens" and len(all_results) >= 2:
            prev_exec = all_results[-2]["token_usage"]["execution"]["total_tokens"]
            curr_exec = result["token_usage"]["execution"]["total_tokens"]
            if prev_exec > 0:
                change_pct = abs(prev_exec - curr_exec) / prev_exec * 100
                if change_pct < 5:
                    print(f"\n  Token change negligible ({change_pct:.1f}%) — stopping token optimisation.")
                    break

        # -- Evolution step --
        if args.evolve and i < args.runs:
            # Determine min_score for token optimisation
            effective_min = min_score
            if effective_min is None and current_optimize == "tokens":
                effective_min = best_score
                print(f"\n  Using best score ({effective_min}) as minimum threshold.")

            new_content, evolve_usage = evolve_command(
                args.command, result["command_output"],
                result["scores"], args.model,
                criteria_content=criteria_content,
                optimize=current_optimize,
                token_usage=result["token_usage"],
                min_score=effective_min,
            )

            # Extract any helper scripts the evolution step produced
            new_content, scripts = extract_scripts(new_content)

            # Write the evolved command
            command_path.write_text(new_content, encoding="utf-8")
            print(f"  Command updated ({evolve_usage['total_tokens']:,} tokens)")

            # Write any helper scripts
            if scripts:
                SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
                for script_path, script_content in scripts.items():
                    out = SCRIPTS_DIR / Path(script_path).name
                    out.write_text(script_content, encoding="utf-8")
                    print(f"  Script written: {out.relative_to(ROOT_DIR)}")

            # Track cumulative usage
            result["token_usage"]["evolution"] = evolve_usage

    # Ensure the best version is the final state
    if args.evolve and all_results and best_iter > 0:
        final_score = all_results[-1]["scores"].get("total", 0)
        if final_score < best_score:
            command_path.write_text(best_content, encoding="utf-8")
            print(f"\n  Final command set to iteration {best_iter} (best score: {best_score})")

    # Summary
    if len(all_results) > 1:
        print(f"\n{'='*60}")
        print("  Evolution Summary")
        print(f"{'='*60}")

        # Build table rows
        rows = []
        total_cost = 0
        for r in all_results:
            total = r["scores"].get("total", 0)
            max_possible = r["scores"].get("max_possible", "?")
            pct = f"{total / max_possible * 100:.0f}%" if isinstance(max_possible, (int, float)) and max_possible > 0 else "?"
            score_str = f"{total}/{max_possible} ({pct})"
            if r["iteration"] == best_iter:
                score_str += " *"

            exec_tokens = r["token_usage"]["execution"]["total_tokens"]
            score_tokens = r["token_usage"]["scoring"]["total_tokens"]
            evolve_tokens = r["token_usage"].get("evolution", {}).get("total_tokens", 0)
            iter_total = exec_tokens + score_tokens + evolve_tokens

            cost = r["token_usage"]["combined"].get("cost_usd", 0)
            evolve_cost = r["token_usage"].get("evolution", {}).get("cost_usd", 0)
            total_cost += cost + evolve_cost

            rows.append({
                "iter": str(r["iteration"]),
                "score": score_str,
                "exec": f"{exec_tokens:,}",
                "score_tok": f"{score_tokens:,}",
                "evolve": f"{evolve_tokens:,}" if evolve_tokens else "-",
                "total_tok": f"{iter_total:,}",
            })

        # Column headers and widths
        headers = {
            "iter": "Iter",
            "score": "Score",
            "exec": "Exec Tokens",
            "score_tok": "Score Tokens",
            "evolve": "Evolve Tokens",
            "total_tok": "Total Tokens",
        }
        col_widths = {
            k: max(len(headers[k]), *(len(r[k]) for r in rows))
            for k in headers
        }

        # Print table
        header_line = "  ".join(h.rjust(col_widths[k]) for k, h in headers.items())
        separator = "  ".join("-" * col_widths[k] for k in headers)
        print(f"\n    {header_line}")
        print(f"    {separator}")
        for r in rows:
            row_line = "  ".join(r[k].rjust(col_widths[k]) for k in headers)
            print(f"    {row_line}")

        if best_iter > 0:
            print(f"\n    Best iteration: {best_iter} (score: {best_score})")
            print("    (* = best)")

        # Score change (first -> best)
        first = all_results[0]["scores"].get("total", 0)
        delta = best_score - first
        sign = "+" if delta > 0 else ""
        print(f"    Score change: {sign}{delta} ({first} -> {best_score})")

        # Execution token trend
        exec_list = [r["token_usage"]["execution"]["total_tokens"] for r in all_results]
        first_exec = exec_list[0]
        last_exec = exec_list[-1]
        exec_delta = last_exec - first_exec
        exec_sign = "+" if exec_delta > 0 else ""
        print(f"    Exec tokens change: {exec_sign}{exec_delta:,} ({first_exec:,} -> {last_exec:,})")

        grand_total_tokens = sum(
            r["token_usage"]["combined"]["total_tokens"]
            + r["token_usage"].get("evolution", {}).get("total_tokens", 0)
            for r in all_results
        )
        print(f"    Total tokens used: {grand_total_tokens:,}")
        if total_cost:
            print(f"    Total cost: ${total_cost:.4f}")


if __name__ == "__main__":
    main()
