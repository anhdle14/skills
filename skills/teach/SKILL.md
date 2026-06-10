---
name: teach
description: Teach a stateful learning topic through mission-grounded, cited lessons and durable learning records. Use when the user says teach me, learn with me, tutor me, create a course, build lessons, or asks for a multi-session learning workspace.
tags: [productivity, create, writing]
args: "<what the user wants to learn>"
---

# Teach

Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.

Use this when the user wants a teacher over multiple sessions, not a one-off answer. Treat the current directory as the teaching workspace.

Adapted from Matt Pocock's `teach` skill structure.

## Workspace Files

Create files lazily, then re-read the relevant ones before each teaching decision.

- `MISSION.md` — why the user is learning and what success looks like. Use [MISSION-FORMAT.md](MISSION-FORMAT.md).
- `RESOURCES.md` — trusted knowledge sources and wisdom/community sources. Use [RESOURCES-FORMAT.md](RESOURCES-FORMAT.md).
- `NOTES.md` — teaching preferences, constraints, and scratch notes that should persist.
- `GLOSSARY.md` — canonical terms the user has demonstrated. Use [GLOSSARY-FORMAT.md](GLOSSARY-FORMAT.md).
- `lessons/*.html` — self-contained lessons, numbered `0001-slug.html`, `0002-slug.html`, etc.
- `reference/*.html` — quick-reference sheets, diagrams, checklists, snippets, routines, or cheat sheets.
- `learning-records/*.md` — durable evidence of non-obvious learning, numbered `0001-slug.md`. Use [LEARNING-RECORD-FORMAT.md](LEARNING-RECORD-FORMAT.md).

## Teaching Workflow

1. **Rehydrate state** — read `MISSION.md`, `RESOURCES.md`, `NOTES.md`, `GLOSSARY.md`, recent learning records, and the file lists under `lessons/` and `reference/` if they exist.
2. **Ground the mission** — if `MISSION.md` is missing, vague, or stale, interview the user before teaching. Confirm before creating or revising it.
3. **Acquire knowledge** — use high-trust sources in `RESOURCES.md`. If sources are missing or weak, research first and update `RESOURCES.md` with annotated links before making strong claims.
4. **Pick the next lesson** — choose one tightly scoped thing tied to the mission and inside the user's zone of proximal development.
5. **Create the lesson** — save one beautiful, self-contained HTML file in `lessons/` with citations, anchors to related local files, and a single command to open it.
6. **Build a feedback loop** — include an interactive quiz, small task, scenario question, checklist, or real-world exercise so the user can practice and receive quick feedback.
7. **Compress for reuse** — when useful, create or update `reference/*.html` and `GLOSSARY.md` so future lessons can link to stable language and quick-reference material.
8. **Record learning only after evidence** — write a learning record when the user demonstrates understanding, discloses prior knowledge, corrects a misconception, or shifts the mission.

## Lesson Rules

- Teach one thing only; give the user a tangible win quickly.
- Prefer skill acquisition over encyclopedic coverage. Explain only the knowledge needed for the practice loop.
- Cite sources for factual claims and include paths to any local references used.
- Make the lesson printable and revisitable: clean typography, semantic HTML, no external runtime dependency unless justified.
- Add a reminder that the user can ask the agent follow-up questions.
- Link lessons and references with relative HTML anchors.

## Wisdom and Community

Wisdom comes from real-world interaction. When the user's question requires lived judgment, answer what you can, then suggest high-reputation communities, mentors, classes, forums, or practitioners from `RESOURCES.md`. Respect any recorded preference to avoid communities.

## Boundaries

- Do not rely on parametric memory when durable resources are needed.
- Do not create a learning record for material merely covered; coverage is not learning.
- Do not mix unrelated topics in one workspace. Ask the user to choose one mission or create separate workspaces.
- Do not overwrite mission or notes silently; confirm changes that alter the learning direction.

## Output

Each turn should state: files read, files changed, the next practice action, and the command to open any new lesson. If blocked by a missing mission or weak resources, ask the smallest question that unblocks teaching.
