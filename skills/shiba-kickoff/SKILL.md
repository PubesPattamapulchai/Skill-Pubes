---
name: shiba-kickoff
description: Kick off work on a project by surveying it for existing context, grilling the user for scope when there's nothing to build on, then drafting a plan of scoped sub-agents (model + skills per scope) and carrying it through build, test, and code review with the superpowers skills. Use when starting new or unclear work in a project, when asked to "kick off"/"bootstrap" a project, or when asked to split a goal into parallel agents with appropriate models.
---

# /shiba-kickoff

Turn "start working on this" into finished, reviewed work: survey what already exists, fill the gaps by grilling the user, draft an agent plan (model + skills per scope), then build it, test it, and code-review it without stopping to ask again. The `superpowers:*` skills drive Steps 5-8; if the superpowers plugin isn't installed, fall back to `shiba-build-loop` (or `shiba-build-loop-ui` for web UI work) for Steps 5-6 and the `code-review` skill for Step 7.

## What You Must Do When Invoked

Follow these steps in order.

### Step 1 — Survey the project

Check, in the current working directory:

- `CLAUDE.md` / `AGENTS.md` / `README*`
- a manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, ...)
- `graphify-out/graph.json` — if present, prefer it: run `graphify query "<question>"` (see the `graphify` skill) instead of grepping files by hand
- existing `.claude/agents/` and `.claude/skills/` in the project
- `git log --oneline -10` and a top-level directory listing

**Completion criterion:** you can state, in one paragraph, either (a) what this project is, what state it's in, and what a next unit of work plausibly is, or (b) that there is nothing here to build that understanding from (no real README/CLAUDE.md content, no source beyond a bare scaffold, trivial or no git history).

### Step 2 — Grill for scope wherever the survey leaves gaps

If Step 1 lands on (b), or lands on (a) but the goal/scope for *this* session is still unstated or ambiguous: call the Skill tool with `"grilling"` and let it interview the user down to a settled design tree. Feed it what Step 1 already found so it doesn't re-ask what's already known.

Do not invent scope the user hasn't confirmed. Skip this step outright only when Step 1 already yields a clear, unambiguous next task.

**Completion criterion:** the grilling session's frontier is empty (per its own completion rule), or Step 1 already made this step unnecessary.

### Step 3 — Draft the agent plan

Break the settled scope into units of work small enough for one sub-agent each. For each unit, decide:

- **Scope**: a one-line goal plus the boundary of what it does *not* cover.
- **Model** — pick the cheapest model that can still do the job well, using `references/model-selection.md`. This isn't limited to Claude: a unit can route to a local or other-provider model instead (same reference, "Local and other-provider models") when there's a concrete reason to.
- **Agent type / tools**: `general-purpose` by default; `Explore` or `Plan` for read-only investigation/planning units; `fork` only when the unit genuinely needs this conversation's context; for a non-Claude model, there's no Agent-tool type at all — see the reference.
- **Isolation**: `worktree` when two or more units touch overlapping files and will run in parallel; omit otherwise.
- **Skills**: scan the available-skills listing in context and name any whose description matches the unit's task — pass these as explicit pointers in that unit's prompt, since a spawned agent starts without this conversation's context.

Present the plan as a table: Scope | Goal | Model | Agent type | Skills. Note any dependency order between units (a unit that needs another's output isn't spawned in the same parallel batch).

**Completion criterion:** every settled decision from Step 2 maps to exactly one unit in the table; nothing settled is left unassigned.

### Step 4 — Confirm, or go

- **Step 2 ran a grilling session:** the user already settled scope. Show the table, then continue to Step 5 without waiting.
- **Step 2 was skipped** (the survey alone gave the task): show the table and wait for the user to confirm, drop, merge, or override units. **Do not build before they confirm** — hard stop.

Either way, stop and ask if the plan needs something the settled scope didn't cover.

### Step 5 — Build

1. If on `main`/`master`, call the Skill tool with `superpowers:using-git-worktrees` first.
2. Call the Skill tool with `superpowers:writing-plans` to turn the Step 3 table into an implementation plan.
3. Execute it with `superpowers:subagent-driven-development`. Each Step 3 unit is a task, spawned with the model, agent type, and isolation decided there. A unit routed to a local/other-provider model runs as the direct Bash/PowerShell/WebFetch call instead and its output is folded back like a sub-agent's result. Units with no dependency between them go in one batch; dependent units wait.
4. Tell every implementer to follow `superpowers:test-driven-development`, plus `shiba-build-loop-ui` when the unit touches a web UI.

**Completion criterion:** every unit implemented and committed on the working branch, each with its own tests.

### Step 6 — Test

Call the Skill tool with `superpowers:verification-before-completion`. Run the full test suite, typecheck, lint, and build from a clean state. For a web UI, also run `shiba-ui-verify` over the whole affected flow.

Red → call `superpowers:systematic-debugging` (routine failure: `shiba-root-cause-fix`), fix, rerun everything. Never report green without quoting the command and its output.

**Completion criterion:** full suite and build green, output read.

### Step 7 — Code review

1. Call the Skill tool with `superpowers:requesting-code-review` over the whole branch diff against the settled scope. If the `code-review` skill is installed, run it too.
2. Handle findings with `superpowers:receiving-code-review`: verify each, fix the real ones, push back on the wrong ones.
3. After any fix, redo Step 6, then re-review.

Max 2 review rounds. Still open findings after that: stop and show them to the user.

**Completion criterion:** a review pass with no unresolved real findings, and Step 6 green after the last change.

### Step 8 — Finish

Call the Skill tool with `superpowers:finishing-a-development-branch`. Merge, PR, or discard is the user's call — don't pick for them.
