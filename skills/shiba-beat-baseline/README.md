# shiba-beat-baseline

A [Claude Code](https://claude.com/claude-code) skill for beating a known baseline using only data (and prior experiments) that are already on hand — no new data collection, no live A/B test. Fits DL/ML work racing a baseline (a competition, a benchmark, a prior model version) as well as non-technical optimization.

- **Read everything that already exists first** — task/competition spec, prior notebooks/experiment logs, the baseline's own code/config, the data itself — before proposing anything, so candidates don't re-propose a logged dead end.
- Pin down the baseline, the metric, and the fixed data you're allowed to use.
- Error-analyze the baseline (including an under-fit vs. over-fit read for a trained model), so candidate methods target real failure patterns instead of guesses.
- Generate a broad list of candidate methods, then score each on **Impact × Confidence × Ease (ICE)**.
- Rank into **Do & pilot / Pilot only / Skip** — an explicit list of which methods are worth the risk and which aren't.
- **Pilot the top candidates on held-out data (a proper CV fold, never the leaderboard/test set) before rolling out to everything** — the score is a prediction, not a result, and only a pilot's actual delta earns a full run.

For optimization tasks bounded by a fixed dataset: tuning a model, process, script, ranking, prompt, or set of decisions against a metric that can't be freely re-measured with more data.

## Install

This skill lives in the [Skill-Pubes](../..) collection — see the [top-level README](../../README.md) for the general install steps. Short version:

```sh
git clone https://github.com/PubesPattamapulchai/Skill-Pubes.git
cp -r Skill-Pubes/skills/shiba-beat-baseline "$HOME/.claude/skills/shiba-beat-baseline"
```

(On Windows: `%USERPROFILE%\.claude\skills\shiba-beat-baseline`.) To scope it to one project instead, copy into `.claude/skills/shiba-beat-baseline` at that project's repo root.

## Use

Type `/shiba-beat-baseline`, or describe the task as "here's my baseline and my data, help me beat it" — the skill's description is written to trigger on that on its own.

## License

MIT — see [LICENSE](../../LICENSE).
