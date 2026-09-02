---
name: kickoff
description: Kick off work on a project by surveying it for existing context, grilling the user for scope when there's nothing to build on, then drafting a plan of scoped sub-agents (model + skills per scope) for approval before spawning. Use when starting new or unclear work in a project, when asked to "kick off"/"bootstrap" a project, or when asked to split a goal into parallel agents with appropriate models.
---

# /kickoff

Turn "start working on this" into a set of scoped, right-sized sub-agents: survey what already exists, fill the gaps by grilling the user, draft an agent plan (model + skills per scope), get it approved, then spawn.

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

### Step 4 — Get approval

Show the table. Ask the user to confirm, drop units, merge units, or override a model/skill choice. **Do not spawn anything before they confirm** — this is a hard stop, not a default you can skip when the plan looks obviously right.

### Step 5 — Spawn

For each approved unit: if it's on a Claude tier, call the Agent tool (model + subagent_type + isolation as decided, description, and a prompt that states the scope boundary and names the pointed-to skills). If it's routed to a local/other-provider model, run it as the direct Bash/PowerShell/WebFetch call decided in Step 3 instead, and fold its output back into the plan the same way a sub-agent's result would be used. Units with no dependency between them go in one batch, per the standing guidance on independent tool calls. Units that depend on another's output wait for it.

**Completion criterion:** every approved unit has been spawned, or the user said to stop.
