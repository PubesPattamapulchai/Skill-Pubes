---
name: build-loop
description: Plan a coding task as small, independently-verifiable increments, then implement -> test -> fix one increment at a time -- never starting the next increment while the current one is red or unverified. Use when building a feature, fixing a bug, or making a multi-step change that should be done carefully with thorough testing rather than all at once.
---

# Build Loop

The discipline this skill enforces: **one increment, fully verified, before the next one starts.** Writing a whole feature and then debugging it end-to-end is the failure mode this skill exists to prevent — by the time something breaks you can't tell which of five changes caused it. Small, verified steps trade a little more overhead per step for a lot less time spent untangling failures later.

This skill owns the *loop* — scoping, decomposition, and increment sequencing. It delegates the two sub-disciplines that make each increment trustworthy to their own skills: writing tests that actually catch bugs (`thorough-tests`) and fixing a red result by root cause instead of guessing (`root-cause-fix`). Both are required — call the Skill tool with their name at the point below, don't inline a shortcut version of either.

If `CONTEXT.md` exists, read it for domain vocabulary before naming anything. Check ADRs in the area you're touching.

## Step 0 — Scope and done criteria

State, in your own words, what "done" means for this task: the observable behavior that must exist when you finish, not the code that must exist. Read the code and existing tests around the area you're changing before proposing anything.

If the goal or its boundary is ambiguous, ask, or call the `grilling` skill if it's installed. Do not invent scope.

**Completion criterion:** done-criteria stated as a checklist of observable outcomes, plus what existing behavior must *not* change.

## Step 1 — Decompose into increments

Break the task into an ordered list of increments. Each must be:

- **Small** — if you can't picture the diff before writing it, it's too big.
- **Independently verifiable** — you can name, in one sentence, the concrete check that verifies just this increment. Can't name it? Split further.
- **System-working at the end** — build compiles, existing tests pass, app still runs, even after increment one.

Present the plan before starting:

| # | Increment | Verification check | Notes/risk |
|---|-----------|--------------------|------------|

Order by dependency; put the riskiest or most uncertain increment early — if an assumption is going to break the plan, better to find out on increment 1 than increment 6.

**Completion criterion:** every piece of Step 0's done-criteria maps to at least one increment; nothing out of scope snuck in.

## Step 2 — The loop

Repeat per increment, in order. **Do not start increment N+1 while increment N is red, partial, or unverified.**

1. **Implement only this increment.** Notice something else worth fixing? Add a row to the plan instead of doing it inline — scope creep inside a "small step" is how steps stop being small.
2. **Cover it with tests** — call the Skill tool with `thorough-tests` and apply its checklist to this increment's change.
3. **Run it for real.** Tests, typecheck, lint, build — whatever the project has. Never report green without having executed something and read its output.
4. **Red → fix** — call the Skill tool with `root-cause-fix`. Don't hand-roll a debug loop here; that skill's stop condition is what keeps this from turning into blind thrashing.
5. **Regression check** — run the broader/full test suite, not just this increment's new tests, before marking it done.
6. **Report and move on** — state the increment is done, with the command and result that prove it. Only then start the next one.

**Completion criterion per increment:** implemented, tested, green including the full suite, reported — in that order, no shortcuts.

## Step 3 — Final pass

1. Run the full test suite and build once more from a clean state.
2. Read the complete diff: remove debug prints, temporary TODOs, dead code from abandoned approaches.
3. Re-check Step 0's done-criteria against what actually shipped — confirm nothing was quietly dropped.
4. If the `code-review` skill is installed, run a pass with it — this skill is about correctness-by-construction as you go; a second pass catches what building it didn't reveal.

**Completion criterion:** full suite green, done-criteria checklist fully checked, diff clean of scaffolding.

## When to stop and ask

- The plan from Step 1 turns out to be wrong mid-loop (an increment reveals the decomposition doesn't fit reality).
- A result reveals the *spec itself* is ambiguous or contradictory, not just the code.
- `root-cause-fix`'s stop condition triggers and sharpening the signal still doesn't produce a workable theory.

Stopping to surface one of these costs a message. Silently pushing through it costs the rest of the loop's integrity.
