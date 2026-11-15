---
name: writing
description: Draft, rewrite, proofread, summarize, explain, plan, or improve prose, technical documents, research papers, implementation plans, and substantive user-facing replies. Use whenever the task is primarily about communicating in writing. Do not use for code-only implementation, exact-output requests, or verbatim/mechanical data transfer.
tags: [writing, create, transform, engineering]
args: "<topic, source, draft, or output path (optional)>"
---

Persistence rule: context is volatile RAM; filesystem is durable disk. For substantial artifacts, write decisions, evidence, open questions, progress, and verification to files; re-read them before drafting and before claiming done.

Use [REFERENCE.md](REFERENCE.md) for genre-specific guidance. Consult [STE-GUIDE.md](STE-GUIDE.md) for original-wording clarity practices inspired by the official ASD-STE100 Issue 9. The standard itself is not included; follow [STE-SOURCE.md](STE-SOURCE.md) to obtain a local copy if needed. This is not a compliance check or endorsement.

## Workflow

1. **Identify the task.** Establish audience, purpose, constraints, format, and whether to create, revise, summarize, explain, plan, or proofread. For a brief reply, infer these and answer directly without files, mode announcements, outlines, or process narration.
2. **Ground claims.** Read supplied material and the relevant source of truth. Preserve exact quotations and user constraints. Mark unknowns explicitly; never invent facts, sources, citations, or results.
3. **Choose structure.** Use the smallest structure that serves the reader. For plans, use [PLAN-TEMPLATE.md](PLAN-TEMPLATE.md) and include scope, decisions, phases, exact validation, exit criteria, risks, and open questions. Adapt or omit sections that do not apply.
4. **Draft or edit.** Lead with the answer or finding. Use concrete words, clear sequencing, consistent terms, and appropriate detail. Preserve the author's meaning and voice. Do not impose a paragraph-length limit or per-section approval loop.
5. **Check.** Proofread for correctness, clarity, completeness, tone, and constraints. For technical prose, verify claims against code, config, tests, schemas, or command output. For research, follow [RESEARCH.md](RESEARCH.md). Use the advisory checker when applicable; never distort clear prose to satisfy a heuristic.
6. **Finish.** For substantial work, report files changed, sources checked, remaining unknowns, and verification. For brief replies, provide only the ready-to-use response.

For existing prose, fix structure before sentence polish. Do not overwrite raw notes when a separate deliverable is appropriate. For style-only requests, do not change claims or qualifications. Distinguish substantive assessment from review; use `review` when the user asks whether an artifact is correct, safe, complete, or fit to approve.
