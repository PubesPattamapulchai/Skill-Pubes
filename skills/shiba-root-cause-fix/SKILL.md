---
name: shiba-root-cause-fix
description: Diagnose and fix a failing test, check, or reported bug by finding the actual root cause instead of guess-patching -- with a hard stop before thrashing blindly. Use when a check goes red and needs fixing, when the user reports something broken, or after a fix attempt didn't actually work.
---

# Root-Cause Fix

Guess-patching — changing something plausible and rerunning to see if it worked — burns attempts without narrowing the search. This skill replaces guessing with a falsifiable theory, and gives a stop condition that keeps a stuck loop from turning into thrashing.

## The loop

1. **Read the actual failure output.** The error message, the diff between expected and actual, the stack trace — not a guess at what it probably says.
2. **Form one specific, falsifiable theory of the cause.** State it as a prediction: "If `<X>` is the cause, then `<changing Y>` will make it pass / `<changing Z>` will make it fail differently." If you can't state the prediction, the theory is a vibe — sharpen it or discard it before acting on it.
3. **Make the smallest change that addresses that theory.** Not a broader rewrite "while you're in there" — scoped exactly to the theory, so the rerun actually tests the theory and nothing else.
4. **Rerun and read the result against the prediction**, not just pass/fail — did it fail the way the theory predicted, or differently? A different failure means the theory was wrong even if the original symptom changed.

## Stop condition

After roughly **3 focused attempts** still red: stop. Do not attempt a 4th blind fix. Instead:

- State explicitly what you've ruled out and what you're stuck on.
- Sharpen the signal before trying again: narrow the repro further (cut inputs/steps one at a time until only the load-bearing ones remain), or add one targeted assertion/log at the exact point where behavior diverges from expectation.
- If sharpening the signal doesn't produce a new, better theory, ask the user rather than continuing to guess — they may have context (a recent change, a known-flaky area) that re-ranks the search instantly.

## Scope

This is the lightweight version for routine red-to-green fixing inside a build or review loop — a failing test, a broken check, a reported one-off bug with an obvious reproduction. For a genuinely hard bug (non-deterministic, no clear repro, a performance regression with no baseline), a fuller diagnosis discipline is warranted; use `superpowers:systematic-debugging` or `diagnosing-bugs`, whichever is installed, instead of pushing this one past its scope.
