---
name: beat-baseline
description: Analyze a fixed, non-extendable set of existing data (and everything already tried against it) to find ways to beat a known baseline on some metric -- generates candidate methods, scores each by expected uplift vs. time/effort and risk, ranks them worth-it vs. not-worth-it, and pilots the cheapest high-signal candidates on held-out data before committing to a full run. Fits DL/ML tasks racing a baseline (a competition, a benchmark, a prior model version) as well as non-technical optimization bounded by whatever data already exists. Use when the data/experiments already available are fixed and the job is to beat a known number with them.
---

# Beat Baseline

Improving something past a known baseline, using only the data already on hand, is a different problem from open-ended optimization: you can't collect more data or run a live experiment to settle disagreements, so every candidate method has to be judged on *expected* payoff against a fixed evidence budget, and validated by holding some of that fixed data back rather than by gathering new data. This skill turns "try to make it better" into a scored, ranked list of methods plus a cheap pilot before any of them gets applied in full.

## Step 1 — Read everything that already exists, before generating anything

Do this first, always — most of the signal for what's worth trying is sitting in what's already been done, not in fresh ideas. Survey, in order:

- **The task/competition description or spec** — the actual metric definition, what counts as the test set, any rules on what's allowed (e.g. external data, ensembling limits).
- **Existing notebooks/scripts/experiment logs** — prior runs, what was tried, what score each attempt got, and any notes on why something worked or didn't. Don't re-propose something already tried and logged as a failure unless you can name what would be different this time.
- **The current baseline's own code/config** — model architecture, features, hyperparameters, preprocessing, training procedure, whatever actually produced the number to beat.
- **The data itself** — schema, size, class/label balance, train/val/(public/private) test split logic, known data quality issues.
- **Any leaderboard or scoreboard history** — current best, how it was achieved, and where public and private/held-out evaluation diverge if that distinction exists.

**Completion criterion:** you can summarize, in a short paragraph, what's already been tried, what worked or didn't and why, and exactly how the current baseline was produced — before Step 2.

## Step 2 — Pin down the baseline and the metric

State explicitly:

- **The metric** being optimized, exactly as scored (not an approximation of it).
- **The baseline value** — the number to beat, sourced from Step 1, not restated from memory.
- **The fixed data** available — what exists, how much, and confirmation nothing more can be collected (if more *can* be added cheaply — more labeled data, external datasets allowed by the rules — this skill's constraint doesn't apply; say so and suggest gathering it instead).

**Completion criterion:** one sentence of the form "beat `<baseline value>` on `<metric>` using only `<the data on hand>`."

## Step 3 — Error-analyze the baseline

Before inventing methods, look at *where* the baseline already fails or underperforms, using the fixed data itself:

- Which cases/rows/examples/classes does it get most wrong, or leave most value on the table? For a model: confusion matrix, per-class or per-segment error, worst residuals, misclassified examples read by hand.
- Is the shortfall concentrated (a few patterns explain most of the gap) or diffuse (no pattern, just noise)?
- For a trained model specifically: is the gap an underfitting signal (train and val both weak — capacity/features/training budget is the lever) or an overfitting signal (train strong, val weak — regularization/data/CV is the lever)? This changes which candidates in Step 4 are worth generating at all.

Concentrated failure patterns point straight at high-confidence candidate methods (Step 4); diffuse ones are a signal that big uplifts are unlikely and small, safe wins are the realistic ceiling — factor that into the confidence scores in Step 5 rather than discovering it after committing to a method.

**Completion criterion:** you can name the top 1-3 patterns behind the gap to baseline (or the under/overfitting read), or state that the gap looks diffuse/noisy.

## Step 4 — Generate candidate methods (breadth first)

List every plausible method that operates *only* on the fixed data and whatever's already been tried — don't filter for quality yet. Draw from more than one angle so the list isn't one family of near-duplicates:

- **Direct fixes to the concentrated failure patterns** found in Step 3.
- **Rule/heuristic refinement** — tightening, loosening, or reordering whatever logic produces the baseline.
- **Re-weighting or re-ranking** what's already being scored, without adding inputs.
- **Combining/ensembling** two or more existing signals or methods (or model checkpoints already trained).
- **Borrowing a known technique** from a similar problem or the published literature for this task type (say what it is and why it transfers).
- **For a DL/ML baseline specifically**, also consider: feature engineering from existing raw fields, preprocessing/cleaning fixes, architecture or capacity changes, hyperparameter/optimizer/schedule tuning, regularization changes, loss function better aligned to the metric, cross-validation strategy fixes (if the current split is the problem, not the model), pseudo-labeling or augmentation that only reuses data already in hand (not new collection), calibration/post-processing of existing model outputs.

Rule out — and say why in one line — any method that secretly needs data or evaluation you don't have (more examples, external data the rules forbid, extra leaderboard submissions beyond what's allowed).

**Completion criterion:** a list of candidate methods wide enough to include at least one from most of the angles above, each stated in one sentence, with none repeating something Step 1 already logged as a tried-and-failed dead end.

## Step 5 — Score each candidate

Score every surviving candidate on three axes, 1-5 each:

- **Impact** — expected uplift over baseline *if it works*, on the metric from Step 2.
- **Confidence** — how sure you are it'll actually work, grounded in Step 3's error analysis, Step 1's prior-experiment evidence, or a stated analogy to a known-working technique. A candidate with no evidence behind it gets low confidence, not a hopeful middle score.
- **Ease** — inverse of cost: how little time/effort it takes to implement *and* validate against held-out data (for ML, this includes training/inference compute time, not just coding time).

Compute **ICE = Impact × Confidence × Ease** (range 1-125) and sort descending. Present as a table:

| Method | Impact | Confidence | Ease | ICE | Tier |
|---|---|---|---|---|---|

Assign **Tier** from the score, not from gut feel:

- **Do & pilot** — top of the ranking, no glaring weak axis (a 5-5-1 is not automatically better than a 3-3-3).
- **Pilot only** — decent ICE but Confidence is the weak axis; worth a cheap test, not worth committing to blind.
- **Skip** — low ICE, or Impact/Confidence low enough that even a free implementation isn't worth the validation effort.

**Completion criterion:** every candidate from Step 4 has a score and a tier; the table is sorted by ICE.

## Step 6 — Pilot before rolling out

Never apply a method to all the data (or a full training run) on the strength of its score alone — the score is a prediction, not a result.

1. Validate on a held-out slice **not** used to design the method in Steps 3-4 — for ML this is a proper CV fold or validation split, never the same data the method was tuned against, and never the public leaderboard/test set as a substitute for internal validation (leaderboard probing burns limited submissions and overfits to it). If the data is too small to split meaningfully, say so explicitly — the pilot's result is then weaker evidence, not skippable.
2. Apply each **Do & pilot** (and, time permitting, **Pilot only**) candidate at pilot scale — a quick training run, a subset, a cheap version of the method. Measure the actual delta against baseline on that held-out slice.
3. Compare actual vs. predicted (Impact) uplift:
   - Beats or matches prediction → promote to a full run on all the data.
   - Underperforms or regresses → drop it, and don't reuse its build effort as a reason to keep it ("sunk cost").
4. Only after a candidate clears its pilot does it get applied in full (full training run, full dataset, full process change).

**Completion criterion:** every "Do & pilot" candidate has a pilot result (promoted or dropped) before any full rollout, and the final report states, per method: predicted uplift, actual pilot uplift, and the rollout decision.

## Reporting

Close with the Step 5 table updated with pilot outcomes, and one line per method stating whether it's worth the risk (promoted) or not (skipped/dropped) and why — this is the artifact the user actually wants, not just the improved result.
