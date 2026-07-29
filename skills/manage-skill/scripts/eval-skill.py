#!/usr/bin/env python3
"""Static and model-backed evaluation for skills in this repo.

Static mode needs nothing but Python 3. Trial mode shells out to `pi` and runs
each case in a clean temporary workspace.

  python3 skills/manage-skill/scripts/eval-skill.py --all --static
  python3 skills/manage-skill/scripts/eval-skill.py --skill skills/tech-writing --static
  python3 skills/manage-skill/scripts/eval-skill.py --skill skills/tech-writing --trials 3
  python3 skills/manage-skill/scripts/eval-skill.py --skill skills/tech-writing --compare-without-skill
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
PERSISTENCE_PATTERN = re.compile(r"context is volatile RAM; filesystem is durable disk", re.IGNORECASE)
BODY_SOFT_CAP = 100
BODY_HARD_CAP = 120
DESCRIPTION_CAP = 1024


@dataclass
class Trace:
    text: str = ""
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    loaded_skill: bool = False


@dataclass
class TrialResult:
    case: str
    mode: str
    passed: bool
    failures: list[str] = field(default_factory=list)
    judge_reason: str = ""


def parse_frontmatter(content: str) -> dict[str, str]:
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        raise ValueError("SKILL.md must start with YAML frontmatter")
    fields: dict[str, str] = {}
    current = ""
    for raw in match.group(1).splitlines():
        if raw.startswith((" ", "\t")) or not raw.strip():
            if current:
                fields[current] += " " + raw.strip()
            continue
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        current = key.strip()
        fields[current] = value.strip().strip("\"'")
    return fields


def repo_root(skill: Path) -> Path:
    return skill.resolve().parent.parent


def default_cases_path(skill: Path) -> Path:
    return skill / "evals" / f"{skill.resolve().name}.json"


def index_failures(skill: Path, name: str, human_only: bool, description: str, args: str) -> list[str]:
    agents_md = repo_root(skill) / "AGENTS.md"
    if not agents_md.is_file():
        return []
    text = agents_md.read_text(encoding="utf-8")
    row = next((line for line in text.splitlines() if f"skills/{name}/SKILL.md" in line), "")
    if not row:
        return [f"AGENTS.md has no index row linking skills/{name}/SKILL.md"]
    failures = []
    if f"npx skills add anhdle14/skills@{name}" not in row:
        failures.append(f"AGENTS.md index row for {name} is missing the install command")
    marked = "*(human-only)*" in row
    if marked != human_only:
        state = "marked *(human-only)*" if marked else "not marked *(human-only)*"
        want = "human-only" if human_only else "model-invocable"
        failures.append(f"AGENTS.md index row for {name} is {state} but the skill is {want}")
    # A row that drifts from the frontmatter advertises a trigger contract the skill no longer honors.
    if description and description not in row:
        failures.append(f"AGENTS.md index row for {name} does not repeat the SKILL.md description verbatim")
    if args and f'Args: `"{args}"`' not in row:
        failures.append(f"AGENTS.md index row for {name} is missing the Args suffix")
    return failures


def skill_failures(skill_md: Path) -> tuple[list[str], dict[str, str]]:
    content = skill_md.read_text(encoding="utf-8")
    try:
        fields = parse_frontmatter(content)
    except ValueError as error:
        return [str(error)], {}

    failures: list[str] = []
    name = fields.get("name", "")
    description = fields.get("description", "")
    human_only = fields.get("disable-model-invocation", "").lower() == "true"

    if not NAME_PATTERN.fullmatch(name):
        failures.append(f"invalid skill name: {name!r}")
    if skill_md.parent.name != name:
        failures.append(f"name {name!r} must match directory {skill_md.parent.name!r}")
    if not description:
        failures.append("description is required")
    elif len(description) > DESCRIPTION_CAP:
        failures.append(f"description exceeds {DESCRIPTION_CAP} characters: {len(description)}")
    if not fields.get("tags"):
        failures.append("tags are required")
    if not PERSISTENCE_PATTERN.search(content):
        failures.append("body is missing the persistence rule line")

    lines = len(content.splitlines())
    if lines > BODY_HARD_CAP:
        failures.append(f"SKILL.md is {lines} lines; hard cap is {BODY_HARD_CAP} - disclose detail to a sibling file")
    elif lines > BODY_SOFT_CAP:
        print(f"WARN {skill_md}: {lines} lines exceeds the {BODY_SOFT_CAP}-line target", file=sys.stderr)

    for link in LINK_PATTERN.findall(content):
        if re.match(r"^(?:https?://|mailto:|#)", link):
            continue
        target = link.split("#", 1)[0]
        if target and not (skill_md.parent / target).exists():
            failures.append(f"broken local reference: {link}")

    failures.extend(index_failures(skill_md.parent, name, human_only, description, fields.get("args", "")))
    return failures, {"name": name, "human_only": str(human_only)}


def suite_failures(cases_path: Path, human_only: bool, required: bool) -> list[str]:
    if not cases_path.is_file():
        if required:
            return [f"missing eval cases: {cases_path}"]
        print(f"WARN no eval cases at {cases_path}", file=sys.stderr)
        return []
    try:
        suite = json.loads(cases_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"invalid eval JSON: {error}"]

    cases = suite.get("cases")
    if not isinstance(cases, list) or not cases:
        return ["eval suite must contain a non-empty cases array"]

    failures: list[str] = []
    names: set[str] = set()
    positive = negative = 0
    for index, case in enumerate(cases):
        label = f"case {index + 1}"
        if not isinstance(case, dict):
            failures.append(f"{label} must be an object")
            continue
        case_name = case.get("name")
        if not case_name or case_name in names:
            failures.append(f"{label} has a missing or duplicate name")
        names.add(case_name)
        if not case.get("prompt"):
            failures.append(f"{label} must define prompt")
        if not isinstance(case.get("should_trigger"), bool):
            failures.append(f"{label} must define boolean should_trigger")
        elif case["should_trigger"]:
            positive += 1
        else:
            negative += 1
        startup = case.get("startup", [])
        if not isinstance(startup, list) or any(not isinstance(command, list) for command in startup):
            failures.append(f"{label} startup must be a list of argument arrays")
    if positive == 0:
        failures.append("eval suite requires at least one positive case")
    if negative == 0 and not human_only:
        failures.append("model-invocable skill requires at least one negative trigger case")
    return failures


def static_checks(skill: Path, cases_path: Path, require_cases: bool) -> list[str]:
    skill_md = skill / "SKILL.md" if skill.is_dir() else skill
    if not skill_md.is_file():
        return [f"missing {skill_md}"]
    failures, fields = skill_failures(skill_md)
    if not fields:
        return failures
    human_only = fields.get("human_only") == "True"
    return failures + suite_failures(cases_path, human_only, require_cases)


def assistant_text(message: dict[str, Any]) -> str:
    return "\n".join(
        item.get("text", "")
        for item in message.get("content", [])
        if isinstance(item, dict) and item.get("type") == "text"
    )


def parse_trace(output: str, skill_md: Path) -> Trace:
    trace = Trace()
    expected = str(skill_md)
    for raw in output.splitlines():
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "message_end" and event.get("message", {}).get("role") == "assistant":
            text = assistant_text(event["message"])
            if text:
                trace.text = text
        if event.get("type") == "tool_execution_start":
            call = {"name": event.get("toolName", ""), "args": event.get("args", {})}
            trace.tool_calls.append(call)
            path = str(call["args"].get("path", ""))
            if call["name"] == "read" and path.endswith(expected.split("skills/", 1)[-1]):
                trace.loaded_skill = True
    return trace


def prepare_workspace(case: dict[str, Any], cases_path: Path, workspace: Path) -> None:
    fixture = case.get("workspace")
    if fixture:
        source = (cases_path.parent / fixture).resolve()
        if not source.is_dir():
            raise ValueError(f"workspace fixture not found: {source}")
        shutil.copytree(source, workspace)
    else:
        workspace.mkdir(parents=True)
    for command in case.get("startup", []):
        result = subprocess.run(command, cwd=workspace, capture_output=True, text=True, check=False)
        if result.returncode:
            raise ValueError(f"startup failed: {shlex.join(command)}\n{result.stderr or result.stdout}")


def pi_command(model: str, extra: list[str]) -> list[str]:
    command = [
        "pi", "--mode", "json", "--print",
        "--no-session", "--no-extensions", "--no-skills", "--no-context-files",
    ]
    if model:
        command.extend(["--model", model])
    return command + extra


def is_human_only(skill_md: Path) -> bool:
    try:
        return parse_frontmatter(skill_md.read_text(encoding="utf-8")).get("disable-model-invocation", "").lower() == "true"
    except (OSError, ValueError):
        return False


def human_only_prompt(skill_md: Path, prompt: str) -> str:
    """Inject a human-only skill the way `/skill:name` does.

    The frontmatter is stripped: a prompt starting with `---` would be parsed as
    a CLI flag, not a positional argument.
    """
    body = FRONTMATTER_PATTERN.sub("", skill_md.read_text(encoding="utf-8")).strip()
    return f"{body}\n\nUser: {prompt}"


def run_case(case: dict[str, Any], skill: Path, cases_path: Path, model: str, enabled: bool) -> tuple[Trace, list[str]]:
    """Run one trial. Returns the trace and any deterministic failures.

    A human-only skill never auto-triggers, so its content is injected the way
    `/skill:name` does and the trigger assertion is skipped - those suites
    assert behavior, not triggering.
    """
    skill_md = skill.resolve() / "SKILL.md"
    human_only = is_human_only(skill_md)
    with tempfile.TemporaryDirectory(prefix="skill-eval-") as temp:
        workspace = Path(temp) / "workspace"
        prepare_workspace(case, cases_path, workspace)
        extra = ["--skill", str(skill.resolve())] if enabled else []
        if case.get("tools"):
            extra.extend(["--tools", ",".join(case["tools"])])
        prompt = case["prompt"]
        if enabled and human_only:
            prompt = human_only_prompt(skill_md, prompt)
        extra.append(prompt)
        result = subprocess.run(
            pi_command(model, extra),
            cwd=workspace,
            capture_output=True,
            text=True,
            check=False,
            timeout=int(case.get("timeout_seconds", 300)),
        )
        if result.returncode:
            raise ValueError(f"pi exited {result.returncode}: {(result.stderr or result.stdout)[-2000:]}")
        trace = parse_trace(result.stdout, skill_md)
        return trace, deterministic_failures(case, trace, workspace, check_trigger=enabled and not human_only)


def deterministic_failures(case: dict[str, Any], trace: Trace, workspace: Path, check_trigger: bool) -> list[str]:
    failures: list[str] = []
    if check_trigger and trace.loaded_skill != case["should_trigger"]:
        failures.append(f"trigger={trace.loaded_skill}, want {case['should_trigger']}")
    expect = case.get("expect", {})
    for pattern in expect.get("response_regex", []):
        if not re.search(pattern, trace.text, re.IGNORECASE | re.DOTALL):
            failures.append(f"response missing /{pattern}/")
    for pattern in expect.get("forbid_response_regex", []):
        if re.search(pattern, trace.text, re.IGNORECASE | re.DOTALL):
            failures.append(f"response unexpectedly matched /{pattern}/")
    names = [call["name"] for call in trace.tool_calls]
    for name in expect.get("tool_names", []):
        if name not in names:
            failures.append(f"missing tool call: {name}")
    read_paths = [str(call["args"].get("path", "")) for call in trace.tool_calls if call["name"] == "read"]
    for pattern in expect.get("read_path_regex", []):
        if not any(re.search(pattern, value) for value in read_paths):
            failures.append(f"no read path matched /{pattern}/")
    for relative in expect.get("file_exists", []):
        if not (workspace / relative).exists():
            failures.append(f"expected file missing: {relative}")
    for relative, pattern in expect.get("file_regex", {}).items():
        path = workspace / relative
        if not path.is_file() or not re.search(pattern, path.read_text(encoding="utf-8"), re.DOTALL):
            failures.append(f"file {relative} missing /{pattern}/")
    return failures


def judge(case: dict[str, Any], trace: Trace, model: str) -> tuple[bool, str]:
    criterion = case.get("expect", {}).get("judge")
    if not criterion:
        return True, ""
    prompt = (
        "Judge this agent response against one criterion.\n"
        'Return only JSON: {"pass": true|false, "reason": "brief evidence"}.\n'
        f"Criterion: {criterion}\nResponse:\n{trace.text}\n"
    )
    result = subprocess.run(
        pi_command(model, ["--no-builtin-tools", prompt]),
        capture_output=True, text=True, check=False, timeout=300,
    )
    if result.returncode:
        return False, f"judge failed: {(result.stderr or result.stdout)[-500:]}"
    judged = parse_trace(result.stdout, Path("/nonexistent"))
    match = re.search(r"\{.*\}", judged.text, re.DOTALL)
    if not match:
        return False, "judge did not return JSON"
    try:
        payload = json.loads(match.group(0))
    except json.JSONDecodeError as error:
        return False, f"invalid judge JSON: {error}"
    return bool(payload.get("pass")), str(payload.get("reason", ""))


def run_suite(args: argparse.Namespace, suite: dict[str, Any], skill: Path, cases_path: Path) -> list[TrialResult]:
    selected = [case for case in suite["cases"] if not args.case or case["name"] in args.case]
    trials = args.trials or int(suite.get("trials", 3))
    modes = [("enabled", True)] + ([("baseline", False)] if args.compare_without_skill else [])
    results: list[TrialResult] = []
    for case in selected:
        for mode, enabled in modes:
            for _ in range(trials):
                try:
                    trace, failures = run_case(case, skill, cases_path, args.model, enabled)
                    reason = ""
                    if args.judge and enabled:
                        passed, reason = judge(case, trace, args.model)
                        if not passed:
                            failures = failures + [f"judge: {reason}"]
                    results.append(TrialResult(case["name"], mode, not failures, failures, reason))
                except (OSError, subprocess.TimeoutExpired, ValueError) as error:
                    results.append(TrialResult(case["name"], mode, False, [str(error)]))
    return results


def report(results: list[TrialResult]) -> int:
    grouped: dict[tuple[str, str], list[TrialResult]] = {}
    for result in results:
        grouped.setdefault((result.case, result.mode), []).append(result)
    failed = False
    for (case, mode), trials in grouped.items():
        passed = sum(trial.passed for trial in trials)
        print(f"{case} [{mode}]: {passed}/{len(trials)} passed")
        for trial in trials:
            if not trial.passed:
                failed = mode == "enabled" or failed
                for failure in trial.failures:
                    print(f"  FAIL [{mode}] {failure}")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate a skill with static and model-backed cases")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--skill", type=Path, help="path to a skill directory")
    target.add_argument("--all", action="store_true", help="statically check every skill under skills/")
    parser.add_argument("--cases", type=Path, help="eval suite (default: <skill>/evals/<name>.json)")
    parser.add_argument("--static", action="store_true", help="run static checks only")
    parser.add_argument("--require-cases", action="store_true", help="fail when a skill has no eval suite")
    parser.add_argument("--model", default="")
    parser.add_argument("--trials", type=int)
    parser.add_argument("--case", action="append")
    parser.add_argument("--judge", action="store_true")
    parser.add_argument("--compare-without-skill", action="store_true")
    args = parser.parse_args(argv)

    if args.all:
        root = Path("skills")
        if not root.is_dir():
            print("STATIC FAIL run --all from the repo root (no skills/ directory here)", file=sys.stderr)
            return 1
        status = 0
        for skill_md in sorted(root.glob("*/SKILL.md")):
            skill = skill_md.parent
            failures = static_checks(skill, default_cases_path(skill), args.require_cases)
            if failures:
                status = 1
                for failure in failures:
                    print(f"STATIC FAIL {skill}: {failure}", file=sys.stderr)
            else:
                print(f"{skill}: static checks passed")
        return status

    cases_path = args.cases or default_cases_path(args.skill)
    failures = static_checks(args.skill, cases_path, args.require_cases or not args.static)
    if failures:
        for failure in failures:
            print(f"STATIC FAIL {failure}", file=sys.stderr)
        return 1
    print(f"{args.skill}: static checks passed")
    if args.static:
        return 0
    suite = json.loads(cases_path.read_text(encoding="utf-8"))
    return report(run_suite(args, suite, args.skill, cases_path))


if __name__ == "__main__":
    raise SystemExit(main())
