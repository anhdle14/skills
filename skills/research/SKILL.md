---
name: research
description: "Explores user intent, requirements, and design before implementation. Use when user asks to research, brainstorm, design, create features, build components, add functionality, or modify behavior before implementation."
tags: [analyze, engineering, plan]
args: "<idea, feature, or behavior change (optional)>"
---

# Brainstorming Ideas Into Designs

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

Help turn ideas into fully formed designs and specs through natural collaborative dialogue. Start by understanding the current project, then ask one question at a time, present design options, and get approval before implementation.

<HARD-GATE>
Do NOT invoke any implementation skill, write code, scaffold a project, or take implementation action until you have presented a design and the user has approved it. This applies regardless of perceived simplicity.
</HARD-GATE>

## Anti-Pattern: "This Is Too Simple To Need A Design"

Every project goes through this process. A todo list, single-function utility, or config change still needs a short design. Simple work is where hidden assumptions waste the most time.

## Checklist

Create and complete tasks in this order:

1. **Explore project context** — check files, docs, recent commits, and existing patterns.
2. **Offer visual companion** — only if upcoming questions would benefit from mockups or diagrams; offer it in its own message.
3. **Ask clarifying questions** — one at a time; understand purpose, constraints, and success criteria.
4. **Propose 2-3 approaches** — include trade-offs and lead with your recommendation.
5. **Present design** — scale sections to complexity; get user approval after each section.
6. **Write design doc** — save to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` unless user preferences override.
7. **Spec self-review** — fix placeholders, contradictions, ambiguity, and scope creep inline.
8. **User reviews written spec** — ask user to review the committed spec before planning.
9. **Transition to implementation planning** — invoke writing-plans; do not invoke implementation skills directly.

## Process

**Understand the idea**

- Check the current project state before asking detailed questions.
- If the request contains multiple independent subsystems, stop and decompose it before refining details.
- For scoped work, ask one question per message. Prefer multiple choice when possible, but use open-ended questions when needed.

**Explore approaches**

- Propose 2-3 viable approaches with trade-offs.
- Recommend one option and explain why.
- YAGNI ruthlessly: remove features that do not serve the stated goal.

**Present the design**

- Present architecture, components, data flow, error handling, and testing at the level the work deserves.
- Ask after each section whether it looks right so far.
- If feedback changes the design, revise and validate before moving on.

**Work in existing codebases**

- Follow current structure and patterns.
- Include targeted boundary or clarity improvements only when they directly serve the current goal.
- Do not propose unrelated refactors.

## After the Design

Write the approved design to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` and commit it unless the user has given a different location or workflow.

Self-review the written spec before asking the user to review it:

- **Placeholder scan:** remove TODO, TBD, incomplete sections, and vague requirements.
- **Internal consistency:** confirm requirements, architecture, and feature descriptions agree.
- **Scope check:** ensure the spec is small enough for one implementation plan.
- **Ambiguity check:** choose explicit interpretations where requirements could split two ways.

Then ask the user to review the spec file before implementation planning. If they request changes, update the spec and repeat the self-review. Proceed only once the user approves.

The next step after brainstorming is writing-plans. Do NOT invoke frontend-design, mcp-builder, or any implementation skill directly.

## Key Principles

- One question at a time.
- Multiple choice preferred.
- Explore alternatives before settling.
- Validate incrementally.
- Be flexible and go back when something does not make sense.

## Visual Companion

A browser-based companion is available for mockups, diagrams, and visual options. Offer it only when upcoming questions would be easier to answer visually.

When offering it, send this as its own message and wait for the user's response:

> "Some of what we're working on might be easier to explain if I can show it to you in a web browser. I can put together mockups, diagrams, comparisons, and other visuals as we go. This feature is still new and can be token-intensive. Want to try it? (Requires opening a local URL)"

If they agree, read `skills/research/visual-companion.md` before proceeding. Use the browser for visual choices; use the terminal for text, scope, and trade-off questions.
