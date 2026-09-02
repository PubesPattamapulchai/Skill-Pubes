# shiba-ui-verify

A [Claude Code](https://claude.com/claude-code) skill for verifying a web UI actually works by driving it in a real browser — not by trusting that the code, or a unit test, is enough.

- Navigate to the affected view, drive the exact interaction, and confirm: correct render, correct interaction result, clean console, clean network.
- Check responsive-sensitive changes at two viewport widths minimum.
- Reset state before checking, and capture a screenshot/GIF as evidence.

Used standalone after any UI change, or as a required dependency of [`shiba-build-loop-ui`](../shiba-build-loop-ui).

## Install

This skill lives in the [Skill-Pubes](../..) collection — see the [top-level README](../../README.md) for the general install steps. Short version:

```sh
git clone https://github.com/PubesPattamapulchai/Skill-Pubes.git
cp -r Skill-Pubes/skills/shiba-ui-verify "$HOME/.claude/skills/shiba-ui-verify"
```

(On Windows: `%USERPROFILE%\.claude\skills\shiba-ui-verify`.) To scope it to one project instead, copy into `.claude/skills/shiba-ui-verify` at that project's repo root.

## Use

Type `/shiba-ui-verify`, or ask to check/verify a page in the browser — the skill's description is written to trigger on its own for that, and it's also invoked automatically by `shiba-build-loop-ui`.

## Requires

- The `claude-in-chrome` skill (or equivalent browser-automation tools).
- Optionally, the `run` skill to launch the app.

## License

MIT — see [LICENSE](../../LICENSE).
