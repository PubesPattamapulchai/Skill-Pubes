# shiba-supply-chain-stats

A [Claude Code](https://claude.com/claude-code) skill that computes and interprets descriptive statistics for supply-chain targets — lead time (LT), demand, price, anything numeric — overall and per group.

- **Groups:** year, quarter, month, weekday (from a date column) plus any column you name: material group (matgrp), plant, vendor, ...
- **Stats:** n, mean, median, SD, CV, min/p25/p75/max, skewness, excess kurtosis, outlier count and % (1.5xIQR), zero %.
- **Demand pattern:** `scripts/demand_class.py` classifies each item as smooth / erratic / intermittent / lumpy from ADI and CV² (Syntetos-Boylan cutoffs 1.32 and 0.49), with item and volume share per class.
- **Interpretation:** XYZ-style variability reading, skew and tail meaning, intermittent demand flag, seasonality and group effects, outlier handling advice, safety-stock inputs.

`scripts/group_stats.py` does the math; the skill decides exclusions, runs it, and reports findings with the numbers behind each.

## Install

Part of the [Skill-Pubes](../..) collection — see the [top-level README](../../README.md). Short version:

```sh
cp -r Skill-Pubes/skills/shiba-supply-chain-stats "$HOME/.claude/skills/shiba-supply-chain-stats"
```

## Use

Type `/shiba-supply-chain-stats`, or run it after [`shiba-supply-chain`](../shiba-supply-chain). Script alone:

```sh
python scripts/group_stats.py data.csv --target LT Demand --by MATKL --date PostDate --out stats.csv
```

## Requires

- Python with `pandas` (and `openpyxl` for Excel).

## License

MIT — see [LICENSE](../../LICENSE).
