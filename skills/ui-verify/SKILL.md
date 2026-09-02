---
name: ui-verify
description: Verify a web UI actually works by driving it in a real browser -- correct render, correct interaction result, clean console, clean network, checked at more than one viewport -- instead of trusting that the code or a unit test is enough. Use after any UI change, or when asked to check/verify a page in the browser.
---

# UI Verify

Passing unit tests and code that "looks right" are not the same claim as "it renders and works." A component can pass every test and still render broken, misalign at a different width, throw a silent console error, or fire the wrong request on click — none of which a DOM-less test catches. This is the checklist for closing that gap: it requires actually loading the page and interacting with it, not reasoning about it from the source.

Load the `claude-in-chrome` skill/tools before starting (per that skill's own guidance on loading its tools together).

## Prerequisite — get the app running

- If the project (or a `run` skill) already defines how to launch it, use that.
- Otherwise start it directly and confirm the URL responds before proceeding.

## The check

For the view/interaction under test:

1. **Navigate to the actual affected view** — not one near it.
2. **Drive the exact interaction** — click, type, submit, navigate — the way a user would trigger it. Don't just load the page and eyeball it if the behavior in question is interactive.
3. **Confirm, concretely:**
   - [ ] The view renders correctly — no broken layout, no unstyled flash, nothing missing where output should appear.
   - [ ] The interaction produces the *correct* result, not just *a* result — check the actual state/content/navigation against what was supposed to happen.
   - [ ] Console is clean of new errors/warnings — read it with the console-reading tool and compare against baseline, don't assume silence.
   - [ ] Network calls tied to the change succeeded — check for unexpected 4xx/5xx if it touches fetching or submission.
4. **Responsive-sensitive changes** (layout, spacing, new elements) get checked at two widths minimum — narrow/mobile and normal desktop. Most layout regressions only show up at one of the two.
5. **Reset state before checking** — reload or clear storage so the result isn't riding on state a previous manual click left behind.
6. **Capture evidence** — a screenshot for a static change, a short GIF for a multi-step interaction — attached to whatever "done" report this check is backing.

Never trigger a native `alert`/`confirm`/`prompt` while doing this — it blocks the automation. If a flow requires one, warn before clicking into it, per the `claude-in-chrome` skill's guidance.

## Scope

This checks one view/interaction at a time. To confirm a whole multi-step flow still works end-to-end after several such changes, repeat the check across the full flow in one continuous session rather than only at each individual change's boundary — combined regressions (a modal that opens but doesn't close, a form that validates fields but not the whole submission) only show up that way.
