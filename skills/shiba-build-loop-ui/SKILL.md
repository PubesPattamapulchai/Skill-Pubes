---
name: shiba-build-loop-ui
description: The shiba-build-loop increment discipline for work with a web UI -- every increment is also verified live in a real browser via the shiba-ui-verify skill, not just by automated tests. Use when implementing or fixing a web page/app feature, especially UI logic, layout, or interaction that a unit test alone won't catch.
---

# Build Loop — UI

Everything in the `shiba-build-loop` skill applies unchanged — its Steps 0, 1, and 3, and the implement/run/regression-check/report parts of its Step 2. This skill adds one rule to Step 2's verification gate: **a UI increment isn't done until it's been checked live in a browser**, via the `shiba-ui-verify` skill, in addition to `shiba-thorough-tests`. Passing tests is not the same claim as "it renders and works" — call both skills, don't substitute one for the other.

## Prerequisite

Before the loop starts, get a real instance of the app running — `shiba-ui-verify`'s own prerequisite section covers how. Confirm it once here so the loop doesn't stall mid-increment.

## The loop's extra gate

For every increment that touches rendered output or interaction (skip only for a purely non-visual increment — a utility function, a data transform with no DOM involvement — `shiba-build-loop`'s ordinary gate covers that):

Between `shiba-build-loop`'s "run it for real" and "regression check" steps, call the Skill tool with `shiba-ui-verify` against the view/interaction this increment implements. Treat a failed check the same as a red test: route it through `shiba-root-cause-fix` before moving on.

## Step 3 addition

Before `shiba-build-loop`'s final full-suite run, do one more `shiba-ui-verify` pass across the *entire* affected flow end-to-end, not just the last increment in isolation. Increments that each verified individually can still combine into a broken flow — a modal that opens correctly but doesn't close, a form that validates each field but not the whole submission. This pass is what catches that.

**Completion criterion:** the full flow works end-to-end in one continuous browser session with a clean console throughout, on top of `shiba-build-loop`'s own completion criterion.
