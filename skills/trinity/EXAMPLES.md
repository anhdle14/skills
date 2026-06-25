# Trinity Examples

One end-to-end trace of the tri-role loop in [SKILL.md](SKILL.md), showing role rotation, a real `REVISE` with a specific diagnosis, Verifier isolation, and the accept gate.

---

## Example — "Implement a token-bucket rate limiter"

One coherent task whose correctness is easy to get subtly wrong, so it earns a verify-and-revise loop rather than a single pass.

### Turn 1 — Thinker (reasoning_worker)

Decomposes and states the acceptance criteria, written to `transcript.md`:

```
plan: bucket holds up to `capacity` tokens; refill at `rate`
      tokens per second; allow() consumes one token if available.
acceptance criteria:
  - tokens never exceed capacity after refill
  - a burst up to capacity is allowed, then throttled
  - refill is proportional to elapsed time, not per-call
```

The Thinker stops here — it does not write the implementation.

### Turn 2 — Worker (coding_worker)

Produces the artifact and appends it to `transcript.md`:

```python
class RateLimiter:
    def __init__(self, capacity, rate):
        self.capacity = capacity
        self.rate = rate
        self.tokens = capacity
        self.last = now()

    def allow(self):
        self.tokens = min(self.capacity,
                          self.tokens + (now() - self.last) * self.rate)
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```

### Turn 3 — Verifier (a different worker)

Reads only the code and the criteria from `transcript.md` — not the Worker's reasoning — and judges against each criterion:

```
REVISE: refill never advances `self.last`, so every allow() call
        recomputes elapsed time from the original timestamp and
        over-refills. Set self.last = now() right after computing
        the refill.
```

A specific defect and a fix direction — not "looks off."

### Turn 4 — Worker (retry)

Feeds the diagnosis back. The Worker adds `self.last = now()` immediately after the refill line and re-appends the corrected artifact.

### Turn 5 — Verifier

Re-checks every criterion against the corrected code:

```
ACCEPT
```

### Stop

Accepted on turn 5 of a five-turn budget. Return the limiter, the role trace (Thinker → Worker → Verifier → Worker → Verifier), the final `ACCEPT`, and `turns=5/5`. Re-read `transcript.md` before declaring done.

---

## What this trace demonstrates

- **Role rotation** — Thinker plans, Worker executes, a *different* Verifier judges.
- **Honest verification** — the `REVISE` names a concrete bug and the fix, so the next turn is actionable.
- **Verifier isolation** — the Verifier reads the artifact from the transcript file, not the Worker's reasoning, so it cannot rubber-stamp.
- **Accept gate** — the loop halts the moment the Verifier accepts, well inside the budget.
- **Persistence** — every turn lives in `transcript.md`, re-read before the done check.
