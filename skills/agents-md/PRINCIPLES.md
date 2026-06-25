# Behavioral Principles to Embed

Four principles that prevent the most common agentic-coding failures. Don't
paste all four verbatim into every AGENTS.md — that's bloat. Instead, encode
the ones a given project actually needs, in the project's own words, where they
fit (usually under Conventions or Gotchas). Each has a verification test you can
use to check whether the drafted file actually enforces it.

---

## 1. Think before coding

**Directive:** Surface assumptions, tradeoffs, and confusion instead of
proceeding silently.

- State assumptions explicitly; if uncertain, ask.
- Present multiple interpretations rather than silently picking one.
- Name confusion instead of guessing past it.

**Test:** Does the file push the agent to clarify ambiguity before
implementing?

---

## 2. Simplicity first

**Directive:** Implement only what was requested; no speculative features or
abstractions.

- No features beyond the ask. No abstractions for single-use code.
- No error handling or configurability nobody requested.
- Litmus: "Would a senior engineer call this overcomplicated?"

**Test:** Could the solution be meaningfully reduced without losing required
functionality?

---

## 3. Surgical changes

**Directive:** Edit only what's necessary; match existing style rather than
improving adjacent code.

- Don't "improve" nearby code, comments, or formatting.
- Remove only imports/vars your change orphaned — not pre-existing dead code.
- Every changed line should trace to the request.

**Test:** Does each diff line connect directly to the stated task?

---

## 4. Goal-driven execution

**Directive:** Turn requests into verifiable success criteria before starting.

- Convert "fix the bug" → "write a failing test that reproduces it, then make
  it pass."
- State multi-step plans with explicit verification checkpoints.

**Test:** Can success be verified independently, without further clarification?

---

## How to encode without bloat

- A tightly-run project that already does TDD doesn't need #4 spelled out —
  one line ("changes aren't done until the relevant test passes") covers it.
- If the repo's pain is over-engineering, lead with #2 and skip the rest.
- Prefer one project-specific imperative over four generic paragraphs. The
  principles are the *why*; the AGENTS.md line is the *rule*.
