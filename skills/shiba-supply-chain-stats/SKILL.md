---
name: shiba-supply-chain-stats
description: Compute and interpret descriptive statistics (mean, SD, CV, outliers, skewness, kurtosis) of supply-chain targets such as lead time (LT) and demand, overall and grouped by month, quarter, year, weekday, material group (matgrp), plant, vendor, or any other column. Use after reading a supply-chain dataset with shiba-supply-chain, or when asked for demand/LT variability, outlier, seasonality, or XYZ-style statistics by group.
---

# Supply Chain Stats

Numbers for the planner: how big is the target, how much does it vary, where is it odd, and which groups differ. `scripts/group_stats.py` computes the numbers; this skill decides what to feed it and reads the result honestly.

Reply in the user's language. Keep column names and numbers verbatim.

## Step 1 — Settle the inputs

Need: the file, the **target** column(s) (LT, Demand, price, ...), the **group-by** columns (matgrp, plant, vendor, ...), and the **date column** if time groupings are wanted (it adds year, quarter, month, weekday).

If `shiba-supply-chain` already ran, take these from its report, including what it said each column means. If the meaning of the target or date is still unconfirmed (planned vs actual LT; posting vs order date), ask first: the date picks which month a row lands in, and the target definition changes every number.

**Completion criterion:** target, groupings, date column, and each one's meaning are stated.

## Step 2 — Decide what is excluded

Reversals, cancelled lines, test rows, and sentinel values (999, 9999) distort every statistic. Look for them, state what you'd exclude and how many rows it removes, and **ask before dropping anything that is not obviously junk**. Never drop rows silently. Exclude by writing a filtered copy in the scratchpad, not by editing the user's file.

**Completion criterion:** an exclusion list with row counts, or "none".

## Step 3 — Run

```sh
python scripts/group_stats.py FILE --target LT Demand --by MATKL WERKS --date PostDate --out stats.csv
```

Use `--sheet` for Excel, `--min-n` (default 5) to drop thin groups, `--top` to cap printed rows (the CSV keeps all). Columns: n, mean, median, sd, cv (SD/|mean|), min, p25, p75, max, skew, ex_kurt (excess), outliers and outlier_pct (1.5xIQR rule), zero_pct.

Check the run header: `numeric of N rows` far below N means the target has text or blanks. Fix that before reading any number.

**Completion criterion:** the script ran clean and printed a table per target per grouping.

### Demand pattern classes (Syntetos-Boylan)

When the target is demand and the file has an item key and a date, also run:

```sh
python scripts/demand_class.py FILE --demand Demand --date PostDate --item MATNR WERKS --period M --out classes.csv
```

Demand is summed per item per period (`--period` D/W/M/Q, default M). Per item, from its first demand to the end of the data: **ADI** = periods / periods with demand (cutoff 1.32) and **CV²** = (SD/mean)² of the non-zero period totals (cutoff 0.49). Classes:

| | CV² < 0.49 | CV² ≥ 0.49 |
|---|---|---|
| **ADI < 1.32** | smooth | erratic |
| **ADI ≥ 1.32** | intermittent | lumpy |

`insufficient` = under 2 demand periods. The item key must match the level you plan at (MATNR alone vs MATNR+WERKS); a wrong key blends items. The cutoffs are the published defaults, not tuned to this business. Finer periods add empty periods and raise ADI (smooth monthly can be intermittent weekly), so state which period you used and match it to the planning bucket.

## Step 4 — Read it

| Signal | Reading | Business consequence |
|---|---|---|
| CV < 0.5 / 0.5-1 / > 1 | Conventional X / Y / Z predictability split | Z items need more buffer or a different policy |
| skew > 1, mean well above median | Long right tail: a few big values drag the mean | Plan on median and percentiles, not the mean |
| high ex_kurt | Heavy tails, rare extreme values | SD understates the risk |
| outlier_pct > ~5% | Many extremes, or a bad sub-population | Investigate before using; could be a real spike or a data error |
| zero_pct high (demand) | Intermittent demand (row level; confirm with `demand_class.py`) | Mean-based forecasts mislead |
| class smooth / erratic | Regular timing; erratic has big size swings | Standard forecast works on smooth; erratic needs buffer for size |
| class intermittent / lumpy | Many empty periods; lumpy also swings in size | Croston/SBA-type methods or order-driven stocking; report class share of items AND of volume |
| group means differ more than within-group SD | Real group effect likely | Plan per group; else treat groups alike |
| n small | Any statistic is shaky | Say so; don't rank on it |

Look for: months/quarters with systematically higher mean or CV (seasonality); weekday effects; groups with the highest CV and highest volume; groups where outliers concentrate. A gap between groups is only a finding if it is large against the spread within them, or tested (e.g. Kruskal-Wallis) when the user asks. Otherwise call it "suggestive".

For safety-stock use, the inputs are the demand mean and SD and the LT mean and SD: standard form `SS = z * sqrt(LT_mean * SD_demand^2 + demand_mean^2 * SD_LT^2)`, valid when demand and LT are independent and in the same time unit. Say which assumption you did not check.

**Completion criterion:** every claim cites a number from the table.

## Step 5 — Report

1. Inputs and exclusions (one short block).
2. Overall stats for each target.
3. Standout groups per grouping: highest and lowest mean, highest CV, most skewed, most outliers. Table, not prose.
4. Three to five findings, each with the number and its business meaning.
5. What to do about outliers: investigate / keep / cap, per group, with the reason. Never drop them without saying.
6. Caveats: small n, ungrouped confounders, untested assumptions. Point to the `--out` CSV.

**Completion criterion:** a planner can act on the findings without reopening the data.

## Common mistakes

| Mistake | Fix |
|---|---|
| Reporting the mean of a skewed target as "typical" | Lead with the median; show the mean as the tail's pull |
| Comparing CV across groups with tiny n | Drop with `--min-n` or flag |
| Averaging group averages | Use the overall row, which weights by n |
| Calling a month "seasonal" from one year of data | Say "one year only; can't separate season from one-off" |
| Treating CV as meaningful when the mean is near 0 | Report it as unstable; the script leaves it blank at mean 0 |
