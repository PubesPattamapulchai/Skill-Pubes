# shiba-ui-theme

A [Claude Code](https://claude.com/claude-code) skill for designing (or restyling) a UI so its visual language comes from what the project is actually about, instead of defaulting to generic style.

- Reads the project's actual subject/content first — not the skill name or framework — to find the theme signal (anime, football, noir, finance, whatever it is).
- Builds an explicit theme profile before touching layout: mood, palette cues drawn from the domain itself, structural motifs, type pairing, and voice.
- Guards the theme against two failure modes: readability/contrast getting sacrificed for style, and cliché decoration standing in for a real motif.
- Falls back to a clean neutral baseline when the project genuinely has no distinctive subject, instead of forcing a theme that isn't there.

Used standalone before any UI/visual design pass, or as the theme-setting step ahead of the `design`, `dataviz`, or `artifact-design` skills, which take the resulting profile and build with it.

## Install

This skill lives in the [Skill-Pubes](../..) collection — see the [top-level README](../../README.md) for the general install steps. Short version:

```sh
git clone https://github.com/PubesPattamapulchai/Skill-Pubes.git
cp -r Skill-Pubes/skills/shiba-ui-theme "$HOME/.claude/skills/shiba-ui-theme"
```

(On Windows: `%USERPROFILE%\.claude\skills\shiba-ui-theme`.) To scope it to one project instead, copy into `.claude/skills/shiba-ui-theme` at that project's repo root.

## Use

Type `/shiba-ui-theme`, or just ask for a UI/design pass on a themed project — the skill's description is written to trigger on its own for that.

## Requires

Nothing on its own. Pairs with `design`, `dataviz`, or `artifact-design` to actually build the UI once the theme profile is set.

## License

MIT — see [LICENSE](../../LICENSE).
