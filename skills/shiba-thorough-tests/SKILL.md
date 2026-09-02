---
name: shiba-thorough-tests
description: Write or review tests that actually catch bugs -- happy path, edge/boundary cases, invalid input, and regressions, with no tautological or implementation-coupled assertions. Use when writing tests for new code, when told tests aren't thorough enough, or when a step in a larger plan calls for verifying a change before moving on.
---

# Thorough Tests

A test that only checks the happy path, or that recomputes its own expected value, passes without proving anything. This skill is the checklist and the anti-patterns that make a test worth keeping.

## The coverage checklist

Before treating a piece of behavior as tested, cover whichever of these apply:

- [ ] **Happy path** — the normal, expected case.
- [ ] **Edge/boundary case** — empty input, zero, max length, first/last element, an off-by-one boundary.
- [ ] **Invalid/error input** — a case the code is *supposed* to reject or handle, not just crash on.
- [ ] **Regression** — anything existing this change touches, so a break shows up now, not later.

Not every function needs all four — a pure, boundary-free helper may have no "edge case" — but check off which apply rather than skipping the thought.

## Anti-patterns

- **Tautological.** The assertion recomputes the expected value the way the code does (`expect(f(x)).toBe(f(x))`, a hand-derived snapshot using the same formula, a constant asserted equal to itself). It passes by construction and can never disagree with the code. The expected value must come from an independent source: a known-good literal, a worked example, the spec.
- **Implementation-coupled.** Mocks internal collaborators, tests private methods, or reads a side channel (querying the database directly instead of going through the interface) instead of asserting through the public interface. The tell: it breaks on a refactor even though behavior didn't change.
- **Vague failure.** An assertion that only proves "didn't crash" (`expect(result).toBeDefined()`) when a specific value was knowable. If you can state the expected value, assert it.

## No test framework in the project

Don't skip verification — build the tightest feedback loop available instead: a script, REPL, or CLI invocation that exercises the real code path and produces a visible pass/fail signal, even if it's never committed as a formal test. A verified-by-hand claim without a command you actually ran doesn't count.

## Running them

Never report a test (or a checklist item above) as satisfied without having actually executed something and read its output. Quote the command and the result.
