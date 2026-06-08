---
name: workflow
description: >
  Apply one of six composable agentic workflow patterns correctly. Use when
  designing multi-step agent pipelines, choosing how to structure parallel or
  iterative work, chaining patterns together, asking how to structure agent work,
  saying "workflow", or mentioning classify and act, fan out, adversarial
  verification, generate and filter, tournament, or loop until done.
tags: [plan, engineering, productivity]
---

# Workflow Patterns

Six patterns. Each has a hard boundary. See [REFERENCE.md](REFERENCE.md) for
full definitions, anti-confusion notes, and failure modes.

## When a Single Prompt Is Enough

Do NOT reach for a workflow pattern if:

- The task fits in one context window with room to spare
- No external tools, data fetches, or side effects are needed
- Quality can be assessed in the same pass that produces the output
- Failure is cheap and retrying manually is fine

Workflows add latency, token cost, and coordination complexity. Only use them
when the single-prompt ceiling is the actual bottleneck.

## Quick Reference

| Pattern | Shape | Hard constraint |
|---------|-------|-----------------|
| **Classify and Act** | input → ONE branch executes | Only one branch runs |
| **Fan Out and Synthesize** | input → N parallel agents → merged output | ALL branches run; results combined |
| **Adversarial Verification** | claim → adversary attacks → surviving claim | Adversary goal is to INVALIDATE |
| **Generate and Filter** | input → many candidates → filtered set | Criteria are absolute, pre-defined |
| **Tournament** | candidates → head-to-head → winner | Comparison is RELATIVE, not absolute |
| **Loop Until Done** | attempt → eval exit condition → refine | Iterative; exit condition explicit upfront |

## Choosing a Pattern

- Input has fundamentally different types requiring different handling? → **Classify and Act**
- Task splits into independent dimensions, all results needed? → **Fan Out and Synthesize**
- Output must survive attack or disproof? → **Adversarial Verification**
- Need breadth first, then narrow by known rules? → **Generate and Filter**
- Quality easier to judge comparatively than by threshold? → **Tournament**
- Quality threshold known but iteration count unknown? → **Loop Until Done**

## Chaining Patterns

Patterns compose. Valid chains and their purpose:

| Chain | When to use |
|-------|-------------|
| Classify → Fan Out | Route to a parallel handler per category |
| Generate and Filter → Tournament | Filter removes invalid; tournament picks best from finalists |
| Adversarial → Loop Until Done | Adversary surfaces flaw; loop drives generator to fix it |
| Fan Out → Loop Until Done | Parallelize subtasks; refine each until it converges |
| Classify → Loop Until Done | Route to the right retry strategy per input type |

**Rule:** each pattern's exit condition must be explicit before handing off to
the next. Never let a loop hand off to a tournament mid-iteration.

See [REFERENCE.md](REFERENCE.md) for chaining anti-patterns.
