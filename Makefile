# Makefile — self-contained repo tooling
# Works on macOS and Linux. Requires: git, deno, markdownlint (npm/brew)
#
# Quickstart on a fresh machine:
#   make bootstrap   → clone, install deno, symlink skills
#   make install     → symlink skills/ to ~/.claude/skills and ~/.agent/skills
#   make lint        → check all markdown
#   make check       → type-check install.ts
#   make ci          → run everything CI runs (lint + check + validate)

.PHONY: bootstrap install copy lint lint-fix check update-index validate ci help

DENO        ?= deno
MDLINT      ?= markdownlint
MDLINT_CONF  = .markdownlint.json
MD_FILES     = README.md CLAUDE.md $(wildcard skills/*/SKILL.md)

## bootstrap: one-shot setup on a fresh machine (clone + install + symlink)
bootstrap:
	@sh bootstrap.sh

## install: symlink skills/ to ~/.claude/skills and ~/.agent/skills
install:
	$(DENO) run --allow-read --allow-write --allow-env=HOME install.ts

## copy: copy skills to a project — usage: make copy DEST=/path/to/project [SKILLS="diagnose grill-me"]
copy:
	@if [ -z "$(DEST)" ]; then echo "Usage: make copy DEST=/path/to/project [SKILLS=\"skill1 skill2\"]"; exit 1; fi
	@if [ -n "$(SKILLS)" ]; then \
		$(DENO) run --allow-read --allow-write --allow-env=HOME install.ts --copy-to $(DEST) \
			$(foreach s,$(SKILLS),--skill $(s)); \
	else \
		$(DENO) run --allow-read --allow-write --allow-env=HOME install.ts --copy-to $(DEST); \
	fi

## update-index: regenerate the skills table in CLAUDE.md
update-index:
	$(DENO) run --allow-read --allow-write --allow-env=HOME install.ts --update-index

## check: type-check install.ts
check:
	$(DENO) check install.ts

## lint: check all markdown files
lint:
	$(MDLINT) --config $(MDLINT_CONF) $(MD_FILES)

## lint-fix: auto-fix markdown violations where possible
lint-fix:
	$(MDLINT) --config $(MDLINT_CONF) --fix $(MD_FILES)

## validate: check every SKILL.md has required frontmatter
validate:
	@fail=0; \
	for f in skills/*/SKILL.md; do \
		skill=$$(dirname "$$f" | xargs basename); \
		if ! grep -q "^name:" "$$f"; then echo "FAIL: $$f missing 'name:'"; fail=1; fi; \
		if ! grep -q "^description:" "$$f"; then echo "FAIL: $$f missing 'description:'"; fail=1; fi; \
		if ! grep -q "^tags:" "$$f"; then echo "FAIL: $$f missing 'tags:'"; fail=1; fi; \
	done; \
	if [ $$fail -eq 0 ]; then echo "OK: all skills have valid frontmatter"; fi; \
	exit $$fail

## ci: run all checks (matches GitHub Actions)
ci: check lint validate

## help: print this help
help:
	@grep -E '^## [a-z]' Makefile | sed 's/^## //' | column -t -s ':'
