"""Descriptive stats of numeric target column(s), overall and per group.

python group_stats.py FILE --target LT Demand --by MATKL WERKS --date PostDate [--out stats.csv]
FILE: .csv/.tsv/.xlsx/.xls. --date adds year, quarter, month, weekday groupings.
"""
import argparse
import sys

import numpy as np
import pandas as pd


def load(path, sheet):
    p = path.lower()
    if p.endswith((".xlsx", ".xlsm", ".xls")):
        return pd.read_excel(path, sheet_name=sheet or 0)
    return pd.read_csv(path, sep="\t" if p.endswith(".tsv") else None, engine="python")


def describe(s):
    s = s.dropna()
    n = len(s)
    mean = s.mean() if n else np.nan
    sd = s.std(ddof=1) if n > 1 else np.nan
    q1, q3 = (s.quantile(0.25), s.quantile(0.75)) if n else (np.nan, np.nan)
    iqr = q3 - q1
    out = ((s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)).sum() if n else 0
    return pd.Series({
        "n": n,
        "mean": mean,
        "median": s.median() if n else np.nan,
        "sd": sd,
        # CV undefined at mean 0; abs() keeps it positive for negative-mean targets
        "cv": sd / abs(mean) if n > 1 and mean != 0 else np.nan,
        "min": s.min() if n else np.nan,
        "p25": q1,
        "p75": q3,
        "max": s.max() if n else np.nan,
        "skew": s.skew() if n > 2 else np.nan,
        "ex_kurt": s.kurt() if n > 3 else np.nan,
        "outliers": int(out),
        "outlier_pct": 100 * out / n if n else np.nan,
        "zero_pct": 100 * (s == 0).mean() if n else np.nan,
    })


def main():
    a = argparse.ArgumentParser()
    a.add_argument("file")
    a.add_argument("--target", nargs="+", required=True)
    a.add_argument("--by", nargs="*", default=[])
    a.add_argument("--date")
    a.add_argument("--sheet")
    a.add_argument("--min-n", type=int, default=5, help="groups smaller than this are dropped")
    a.add_argument("--top", type=int, default=25, help="rows printed per table (CSV gets all)")
    a.add_argument("--out")
    a = a.parse_args()

    df = load(a.file, a.sheet)
    by = list(a.by)
    if a.date:
        d = pd.to_datetime(df[a.date], errors="coerce")
        if d.isna().mean() > 0.2:
            sys.exit(f"--date {a.date}: {d.isna().mean():.0%} unparseable; fix format first")
        df["year"], df["quarter"] = d.dt.year, d.dt.quarter
        df["month"], df["weekday"] = d.dt.month, d.dt.day_name()
        by += ["year", "quarter", "month", "weekday"]
    missing = [c for c in a.target + by if c not in df.columns]
    if missing:
        sys.exit(f"columns not found: {missing}; have: {list(df.columns)}")

    rows = []
    for t in a.target:
        df[t] = pd.to_numeric(df[t], errors="coerce")
        print(f"\n=== {t}: {df[t].notna().sum()} numeric of {len(df)} rows ===")
        overall = describe(df[t]).to_frame().T.astype({"n": int, "outliers": int}).assign(target=t, group_by="(all)", group="(all)")
        rows.append(overall)
        print(overall.drop(columns=["target", "group_by", "group"]).round(3).to_string(index=False))
        for g in by:
            r = df.groupby(g, dropna=False)[t].apply(describe).unstack()
            r = r[r["n"] >= a.min_n].reset_index().rename(columns={g: "group"})
            r = r.astype({"n": int, "outliers": int})
            r.insert(0, "group_by", g)
            r.insert(0, "target", t)
            rows.append(r)
            dropped = df[g].nunique(dropna=False) - len(r)
            note = f" ({dropped} groups below min-n={a.min_n} dropped)" if dropped else ""
            print(f"\n-- {t} by {g}{note}; showing {min(a.top, len(r))} of {len(r)} --")
            print(r.drop(columns=["target", "group_by"]).head(a.top).round(3).to_string(index=False))
    if a.out:
        pd.concat(rows, ignore_index=True).to_csv(a.out, index=False)
        print(f"\nfull table -> {a.out}")


if __name__ == "__main__":
    main()
