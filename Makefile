# Makefile — repo checks for the skills collection
# Works on macOS and Linux. Requires: deno, markdownlint (npm/brew)
#
# Quickstart for using these skills:
#   npx skills add anhdle14/skills -g --all
#
# Local development:
#   make lint        → check all markdown
#   make check       → type-check validation/eval tooling
#   make ci          → run everything CI runs (lint + check + validate)

.PHONY: lint lint-fix check validate ci help

DENO        ?= deno
MDLINT      ?= markdownlint
MDLINT_CONF  = .markdownlint.json
MD_FILES     = README.md AGENTS.md $(wildcard skills/*/SKILL.md)

## check: type-check TypeScript tooling
check:
	$(DENO) check scripts/validate-skills.ts scripts/eval-engineering-skills.ts

## lint: check all markdown files
lint:
	$(MDLINT) --config $(MDLINT_CONF) $(MD_FILES)

## lint-fix: auto-fix markdown violations where possible
lint-fix:
	$(MDLINT) --config $(MDLINT_CONF) --fix $(MD_FILES)

## validate: check every SKILL.md follows the skill schema
validate:
	$(DENO) run --allow-read scripts/validate-skills.ts

## ci: run all checks (matches GitHub Actions)
ci: check lint validate

## help: print this help
help:
	@grep -E '^## [a-z]' Makefile | sed 's/^## //' | column -t -s ':'
