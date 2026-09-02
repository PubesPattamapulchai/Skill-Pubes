# shiba-build-loop

A [Claude Code](https://claude.com/claude-code) skill that turns "build this" into small, verified steps instead of one big batch you debug at the end.

1. **Scopes the task** — states done-criteria as observable outcomes before writing anything, and asks rather than guessing when the goal is ambiguous.
2. **Decomposes into increments** — each one small, independently verifiable (a named check that goes red/green for just that piece), and leaves the system working when it lands.
3. **Loops per increment**: implement only this increment → cover it with tests via [`shiba-thorough-tests`](../shiba-thorough-tests) → run them for real → on red, fix via [`shiba-root-cause-fix`](../shiba-root-cause-fix) → run the full suite before calling the increment done.
4. **Never starts increment N+1 while N is red, partial, or unverified.**
5. **Finishes with a full-suite run, a diff read-through for leftover scaffolding, and a check back against the original done-criteria.**

`shiba-build-loop` owns the loop and the increment discipline; it delegates test-writing and bug-fixing to their own focused skills rather than reimplementing them, so each stays useful on its own outside this loop too.

## Install

This skill lives in the [Skill-Pubes](../..) collection — see the [top-level README](../../README.md) for the general install steps. Short version:

```sh
git clone https://github.com/PubesPattamapulchai/Skill-Pubes.git
cp -r Skill-Pubes/skills/shiba-build-loop "$HOME/.claude/skills/shiba-build-loop"
```

(On Windows: `%USERPROFILE%\.claude\skills\shiba-build-loop`.) To scope it to one project instead, copy into `.claude/skills/shiba-build-loop` at that project's repo root.

## Use

Type `/shiba-build-loop`, or just ask for a feature/fix that should be built carefully — the skill's description is written to trigger on its own for multi-step changes.

For work with a web UI, use [`shiba-build-loop-ui`](../shiba-build-loop-ui) instead — same discipline, plus a real-browser verification gate per increment.

## Requires

- [`shiba-thorough-tests`](../shiba-thorough-tests) — for Step 2's test-coverage gate.
- [`shiba-root-cause-fix`](../shiba-root-cause-fix) — for Step 2's fix-on-red gate.
- Optionally, `grilling` for Step 0 if the goal is ambiguous, and `code-review` for an extra pass in Step 3.

## License

MIT — see [LICENSE](../../LICENSE).
