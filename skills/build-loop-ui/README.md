# build-loop-ui

The [`build-loop`](../build-loop) increment discipline, for work with a web UI. Adds one rule: **a UI increment isn't verified until it's actually been loaded and driven in a real browser** — passing unit tests is not the same claim as "it renders and works."

1. Gets a real instance of the app running before the loop starts.
2. Follows `build-loop`'s scope → decompose → implement → test → fix loop unchanged.
3. Adds a live browser check per increment via [`ui-verify`](../ui-verify): navigate to the actual affected view, drive the exact interaction, confirm correct render, correct result, clean console, clean network — at more than one viewport width for anything layout-related.
4. Before the final full-suite run, does one end-to-end click-through of the whole affected flow via `ui-verify` again, not just the last increment in isolation.

This skill is a thin layer on top of `build-loop` — it doesn't re-teach the increment loop or the browser-check checklist, both live in their own skill so they stay reusable on their own.

## Install

This skill lives in the [Skill-Pubes](../..) collection — see the [top-level README](../../README.md) for the general install steps. Short version:

```sh
git clone https://github.com/PubesPattamapulchai/Skill-Pubes.git
cp -r Skill-Pubes/skills/build-loop-ui "$HOME/.claude/skills/build-loop-ui"
```

(On Windows: `%USERPROFILE%\.claude\skills\build-loop-ui`.) To scope it to one project instead, copy into `.claude/skills/build-loop-ui` at that project's repo root.

## Use

Type `/build-loop-ui`, or ask for a web page/app feature or fix — the skill's description is written to trigger on its own for UI work.

## Requires

- [`build-loop`](../build-loop), [`thorough-tests`](../thorough-tests), [`root-cause-fix`](../root-cause-fix) — the base loop this skill layers on.
- [`ui-verify`](../ui-verify) — the live browser-check gate.
- The `claude-in-chrome` skill (or equivalent browser-automation tools), which `ui-verify` drives.
- Optionally, the `run` skill to launch the app.

## License

MIT — see [LICENSE](../../LICENSE).
