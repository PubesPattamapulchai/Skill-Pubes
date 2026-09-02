# shiba-thorough-tests

A [Claude Code](https://claude.com/claude-code) skill for writing tests that actually catch bugs, instead of tests that just pass.

- A coverage checklist: happy path, edge/boundary case, invalid/error input, regression — checked off per change, not assumed.
- Anti-patterns to avoid: tautological assertions (recomputing the expected value the way the code does), implementation-coupled tests (mocking internals, reaching past the public interface), and vague "didn't crash" assertions where a specific value was knowable.
- A fallback for projects with no test framework: build the tightest feedback loop available instead of skipping verification.

Used standalone, or as a required dependency of [`shiba-build-loop`](../shiba-build-loop) and [`shiba-build-loop-ui`](../shiba-build-loop-ui).

## Install

This skill lives in the [Skill-Pubes](../..) collection — see the [top-level README](../../README.md) for the general install steps. Short version:

```sh
git clone https://github.com/PubesPattamapulchai/Skill-Pubes.git
cp -r Skill-Pubes/skills/shiba-thorough-tests "$HOME/.claude/skills/shiba-thorough-tests"
```

(On Windows: `%USERPROFILE%\.claude\skills\shiba-thorough-tests`.) To scope it to one project instead, copy into `.claude/skills/shiba-thorough-tests` at that project's repo root.

## Use

Type `/shiba-thorough-tests`, or just ask to write or review tests — the skill's description is written to trigger on its own for that, and it's also invoked automatically by `shiba-build-loop`/`shiba-build-loop-ui`.

## License

MIT — see [LICENSE](../../LICENSE).
