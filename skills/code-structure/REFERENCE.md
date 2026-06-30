# Code Structure Reference

Service anti-patterns and review questions for the structure work in [SKILL.md](SKILL.md).
Consult these when evaluating a proposed extraction or reviewing a structure plan; a
map-only run does not need them.

## Watch For

- **God service**: one huge method hides the whole flow and removes caller control.
- **Leaky service**: service reaches into database tables or domain state directly.
- **Inconsistent service API**: every helper has different parameter and error conventions.
- **Premature abstraction**: logic used once is extracted because it "might" be reused.
- **Policy drift**: service starts deciding business rules that callers should own.
- **Map without decision**: orientation that never names the structural change it enables.

## Review Questions

- What module owns the domain concept?
- Does the proposed interface hide meaningful complexity, or just rename it?
- If this service disappeared, would the operation be duplicated across callers?
- Can each caller still express domain rules clearly?
- Are all inputs visible, and are success/failure states explicit?
- Would a bug fix in this operation now apply everywhere it should?
