#!/usr/bin/env python3
"""Tests for the skill eval harness. Run: python3 -m unittest discover -s skills/manage-skill/tests"""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import eval_skill

PERSISTENCE = "Persistence rule: context is volatile RAM; filesystem is durable disk."
DESCRIPTION = "Validate widget configs. Use when the user edits a widget config file."

GOOD_SKILL = f"""---
name: widget-check
description: {DESCRIPTION}
tags: [engineering]
---

# Widget check

{PERSISTENCE}

See [REFERENCE.md](REFERENCE.md).
"""

GOOD_SUITE = {
    "skill": "widget-check",
    "trials": 3,
    "cases": [
        {"name": "positive", "prompt": "Validate my widget config.", "should_trigger": True},
        {"name": "negative", "prompt": "Rename a Go variable.", "should_trigger": False},
    ],
}


def write_skill(root: Path, name: str, body: str, suite: dict | None = GOOD_SUITE) -> Path:
    skill = root / "skills" / name
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(body, encoding="utf-8")
    (skill / "REFERENCE.md").write_text("# reference\n", encoding="utf-8")
    if suite is not None:
        (skill / "evals").mkdir()
        (skill / "evals" / f"{name}.json").write_text(json.dumps(suite), encoding="utf-8")
    return skill


class FrontmatterTest(unittest.TestCase):
    def test_parses_fields_and_continuations(self):
        fields = eval_skill.parse_frontmatter("---\nname: a-b\ndescription: one\n  two\ntags: [x]\n---\nbody\n")
        self.assertEqual(fields["name"], "a-b")
        self.assertEqual(fields["description"], "one two")

    def test_rejects_missing_frontmatter(self):
        with self.assertRaises(ValueError):
            eval_skill.parse_frontmatter("# no frontmatter\n")


class StaticCheckTest(unittest.TestCase):
    def check(self, body: str, name: str = "widget-check", suite: dict | None = GOOD_SUITE) -> list[str]:
        with tempfile.TemporaryDirectory() as temp:
            skill = write_skill(Path(temp), name, body, suite)
            return eval_skill.static_checks(skill, eval_skill.default_cases_path(skill), True)

    def test_good_skill_passes(self):
        self.assertEqual(self.check(GOOD_SKILL), [])

    def test_name_must_match_directory(self):
        body = GOOD_SKILL.replace("name: widget-check", "name: widget-checker")
        self.assertIn("must match directory", " ".join(self.check(body)))

    def test_requires_persistence_rule(self):
        self.assertIn("persistence rule", " ".join(self.check(GOOD_SKILL.replace(PERSISTENCE, "Notes."))))

    def test_reference_skill_needs_no_persistence_rule(self):
        body = GOOD_SKILL.replace("tags: [engineering]", "tags: [engineering, reference]").replace(PERSISTENCE, "Lookup material.")
        self.assertEqual(self.check(body), [])

    def test_reference_skill_rejects_persistence_rule(self):
        body = GOOD_SKILL.replace("tags: [engineering]", "tags: [engineering, reference]")
        self.assertIn("must not carry the persistence rule", " ".join(self.check(body)))

    def test_requires_tags(self):
        self.assertIn("tags are required", " ".join(self.check(GOOD_SKILL.replace("tags: [engineering]\n", ""))))

    def test_rejects_broken_local_link(self):
        body = GOOD_SKILL.replace("[REFERENCE.md](REFERENCE.md)", "[missing](MISSING.md)")
        self.assertIn("broken local reference", " ".join(self.check(body)))

    def test_rejects_oversized_body(self):
        body = GOOD_SKILL + "\n".join(f"line {index}" for index in range(eval_skill.BODY_HARD_CAP + 5))
        self.assertIn("hard cap", " ".join(self.check(body)))

    def test_requires_eval_suite(self):
        self.assertIn("missing eval cases", " ".join(self.check(GOOD_SKILL, suite=None)))

    def test_model_invocable_needs_negative_case(self):
        suite = {"cases": [GOOD_SUITE["cases"][0]]}
        self.assertIn("negative trigger case", " ".join(self.check(GOOD_SKILL, suite=suite)))

    def test_human_only_skill_needs_no_negative_case(self):
        body = GOOD_SKILL.replace("tags:", "disable-model-invocation: true\ntags:")
        suite = {"cases": [GOOD_SUITE["cases"][0]]}
        self.assertEqual(self.check(body, suite=suite), [])

    def test_suite_needs_boolean_should_trigger(self):
        suite = {"cases": [{"name": "a", "prompt": "x"}, GOOD_SUITE["cases"][1]]}
        self.assertIn("boolean should_trigger", " ".join(self.check(GOOD_SKILL, suite=suite)))


class IndexCheckTest(unittest.TestCase):
    def failures(self, row: str, body: str = GOOD_SKILL) -> list[str]:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill = write_skill(root, "widget-check", body)
            (root / "AGENTS.md").write_text(f"| skill | install |\n{row}\n", encoding="utf-8")
            return eval_skill.static_checks(skill, eval_skill.default_cases_path(skill), True)

    def test_missing_row_fails(self):
        self.assertIn("no index row", " ".join(self.failures("| nothing | here |")))

    def test_row_needs_install_command(self):
        row = "| [widget-check](skills/widget-check/SKILL.md) | see docs | desc |"
        self.assertIn("missing the install command", " ".join(self.failures(row)))

    def test_human_only_marker_must_match(self):
        row = "| [widget-check](skills/widget-check/SKILL.md) *(human-only)* | `npx skills add anhdle14/skills@widget-check` | desc |"
        self.assertIn("human-only", " ".join(self.failures(row)))

    def test_matching_row_passes(self):
        row = f"| [widget-check](skills/widget-check/SKILL.md) | `npx skills add anhdle14/skills@widget-check` | {DESCRIPTION} |"
        self.assertEqual(self.failures(row), [])

    def test_row_description_must_match_frontmatter(self):
        row = "| [widget-check](skills/widget-check/SKILL.md) | `npx skills add anhdle14/skills@widget-check` | Validate anything at all. |"
        self.assertIn("does not repeat the SKILL.md description", " ".join(self.failures(row)))

    def test_row_must_carry_args_suffix(self):
        body = GOOD_SKILL.replace("tags:", 'args: "<config path>"\ntags:')
        row = f"| [widget-check](skills/widget-check/SKILL.md) | `npx skills add anhdle14/skills@widget-check` | {DESCRIPTION} |"
        self.assertIn("missing the Args suffix", " ".join(self.failures(row, body)))


class TraceTest(unittest.TestCase):
    def trace(self, path: str) -> eval_skill.Trace:
        events = [
            {"type": "tool_execution_start", "toolName": "read", "args": {"path": path}},
            {"type": "message_end", "message": {"role": "assistant", "content": [{"type": "text", "text": "done"}]}},
        ]
        return eval_skill.parse_trace("\n".join(json.dumps(event) for event in events), Path("/repo/skills/foo/SKILL.md"))

    def test_detects_skill_load(self):
        self.assertTrue(self.trace("/repo/skills/foo/SKILL.md").loaded_skill)

    def test_ignores_other_reads(self):
        parsed = self.trace("/repo/skills/bar/SKILL.md")
        self.assertFalse(parsed.loaded_skill)
        self.assertEqual(parsed.text, "done")


class DeterministicFailureTest(unittest.TestCase):
    def test_trigger_mismatch_reported(self):
        case = {"should_trigger": True}
        trace = eval_skill.Trace(text="hi")
        failures = eval_skill.deterministic_failures(case, trace, Path("/tmp"), check_trigger=True)
        self.assertIn("trigger=False", failures[0])

    def test_baseline_mode_skips_trigger_check(self):
        case = {"should_trigger": True}
        trace = eval_skill.Trace(text="hi")
        self.assertEqual(eval_skill.deterministic_failures(case, trace, Path("/tmp"), check_trigger=False), [])

    def test_response_and_file_assertions(self):
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp)
            (workspace / "out.md").write_text("verified claim\n", encoding="utf-8")
            case = {
                "should_trigger": True,
                "expect": {
                    "response_regex": ["eval"],
                    "forbid_response_regex": ["guess"],
                    "tool_names": ["write"],
                    "file_exists": ["out.md"],
                    "file_regex": {"out.md": "verified"},
                },
            }
            trace = eval_skill.Trace(text="added eval cases", tool_calls=[{"name": "write", "args": {}}], loaded_skill=True)
            self.assertEqual(eval_skill.deterministic_failures(case, trace, workspace, check_trigger=True), [])

            trace.text = "I will guess the defaults"
            failures = eval_skill.deterministic_failures(case, trace, workspace, check_trigger=True)
            self.assertEqual(len(failures), 2, failures)


class HumanOnlyInjectionTest(unittest.TestCase):
    def test_strips_frontmatter_and_appends_user_turn(self):
        with tempfile.TemporaryDirectory() as temp:
            skill = write_skill(Path(temp), "widget-check", GOOD_SKILL)
            prompt = eval_skill.human_only_prompt(skill / "SKILL.md", "do the thing")
        self.assertFalse(prompt.startswith("-"), "a prompt starting with --- is parsed as a CLI flag")
        self.assertNotIn("name: widget-check", prompt)
        self.assertIn(PERSISTENCE, prompt)
        self.assertTrue(prompt.endswith("User: do the thing"))

    def test_detects_human_only_flag(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plain = write_skill(root, "widget-check", GOOD_SKILL)
            human = write_skill(root, "widget-audit", GOOD_SKILL.replace("name: widget-check", "name: widget-audit\ndisable-model-invocation: true"))
            self.assertFalse(eval_skill.is_human_only(plain / "SKILL.md"))
            self.assertTrue(eval_skill.is_human_only(human / "SKILL.md"))


class ReportTest(unittest.TestCase):
    def report(self, results: list) -> int:
        """report() prints its own FAIL lines; capture them so a passing run looks passing."""
        with contextlib.redirect_stdout(io.StringIO()):
            return eval_skill.report(results)

    def test_baseline_failures_do_not_fail_the_run(self):
        results = [
            eval_skill.TrialResult("a", "enabled", True),
            eval_skill.TrialResult("a", "baseline", False, ["response missing /x/"]),
        ]
        self.assertEqual(self.report(results), 0)

    def test_enabled_failure_fails_the_run(self):
        self.assertEqual(self.report([eval_skill.TrialResult("a", "enabled", False, ["boom"])]), 1)


if __name__ == "__main__":
    unittest.main()
