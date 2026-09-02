# shiba-root-cause-fix

A [Claude Code](https://claude.com/claude-code) skill for fixing a red test/check/bug by root cause instead of guess-patching.

- Read the actual failure output before forming a theory.
- State the theory as a falsifiable prediction, not a vibe.
- Make the smallest change scoped to that theory, rerun, and check the result against the prediction — not just pass/fail.
- **Stop after ~3 focused attempts** still red: sharpen the signal (narrow the repro, add a targeted assertion) or ask, rather than trying a 4th blind fix.

This is the lightweight, routine version — for a genuinely hard bug (non-deterministic, no clear repro, a performance regression) reach for a fuller diagnosis skill like `diagnosing-bugs` instead.

Used standalone, or as a required dependency of [`shiba-build-loop`](../shiba-build-loop) and [`shiba-build-loop-ui`](../shiba-build-loop-ui).

## Install

This skill lives in the [Skill-Pubes](../..) collection — see the [top-level README](../../README.md) for the general install steps. Short version:

```sh
git clone https://github.com/PubesPattamapulchai/Skill-Pubes.git
cp -r Skill-Pubes/skills/shiba-root-cause-fix "$HOME/.claude/skills/shiba-root-cause-fix"
```

(On Windows: `%USERPROFILE%\.claude\skills\shiba-root-cause-fix`.) To scope it to one project instead, copy into `.claude/skills/shiba-root-cause-fix` at that project's repo root.

## Use

Type `/shiba-root-cause-fix`, or just report something broken — the skill's description is written to trigger on its own for that, and it's also invoked automatically by `shiba-build-loop`/`shiba-build-loop-ui`.

## License

MIT — see [LICENSE](../../LICENSE).
