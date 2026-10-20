"""Classify demand per item as smooth / erratic / intermittent / lumpy (Syntetos-Boylan).

python demand_class.py FILE --demand Demand --date PostDate --item MATNR [WERKS] [--period M] [--out classes.csv]

Demand is summed per item per period. Per item, over its span from first demand to the end of the data:
  ADI = periods / periods with demand        (cutoff 1.32)
  CV2 = (SD / mean)^2 of the non-zero period totals (cutoff 0.49)
"""
import argparse
import sys

import numpy as np
import pandas as pd

from group_stats import load

ADI_CUT, CV2_CUT = 1.32, 0.49


def label(adi, cv2):
    if np.isnan(cv2):
        return "insufficient"  # fewer than 2 demand periods: CV2 undefined
    if adi < ADI_CUT:
        return "smooth" if cv2 < CV2_CUT else "erratic"
    return "intermittent" if cv2 < CV2_CUT else "lumpy"


def main():
    a = argparse.ArgumentParser()
    a.add_argument("file")
    a.add_argument("--demand", required=True)
    a.add_argument("--date", required=True)
    a.add_argument("--item", nargs="+", required=True, help="column(s) that identify one item, e.g. MATNR WERKS")
    a.add_argument("--period", default="M", choices=["D", "W", "M", "Q"])
    a.add_argument("--sheet")
    a.add_argument("--top", type=int, default=25)
    a.add_argument("--out")
    a = a.parse_args()

    df = load(a.file, a.sheet)
    missing = [c for c in [a.demand, a.date] + a.item if c not in df.columns]
    if missing:
        sys.exit(f"columns not found: {missing}; have: {list(df.columns)}")
    df[a.demand] = pd.to_numeric(df[a.demand], errors="coerce")
    df["_d"] = pd.to_datetime(df[a.date], errors="coerce")
    bad = df[a.demand].isna() | df["_d"].isna()
    if bad.mean() > 0.2:
        sys.exit(f"{bad.mean():.0%} of rows have non-numeric demand or unparseable date; fix first")
    df = df[~bad]
    df["_p"] = df["_d"].dt.to_period(a.period)
    last = df["_p"].max()
    print(f"periods: {df['_p'].min()} .. {last} ({a.period}); items by {a.item}")

    per = df.groupby(a.item + ["_p"])[a.demand].sum().reset_index()
    neg = (per[a.demand] < 0).sum()
    if neg:
        print(f"warning: {neg} item-periods have net negative demand (returns/reversals); treated as no demand")
    per = per[per[a.demand] > 0]

    rows = []
    for key, g in per.groupby(a.item):
        key = key if isinstance(key, tuple) else (key,)
        first = g["_p"].min()
        n_per = (last - first).n + 1
        sizes = g[a.demand]
        n_nz = len(sizes)
        adi = n_per / n_nz
        mean = sizes.mean()
        cv2 = (sizes.std(ddof=1) / mean) ** 2 if n_nz > 1 else np.nan
        rows.append((*key, n_per, n_nz, adi, cv2, mean, sizes.sum(), label(adi, cv2)))
    res = pd.DataFrame(rows, columns=a.item + ["periods", "demand_periods", "adi", "cv2", "mean_size", "total", "class"])
    if res.empty:
        sys.exit("no item has positive demand")

    summ = res.groupby("class").agg(items=("class", "size"), total=("total", "sum"))
    summ["items_pct"] = 100 * summ["items"] / summ["items"].sum()
    summ["volume_pct"] = 100 * summ["total"] / summ["total"].sum()
    print("\n-- classes --")
    print(summ.drop(columns="total").round(1).to_string())
    if (res["periods"] < 12).mean() > 0.5:
        print("warning: most items have under 12 periods of history; classes are unreliable")
    print(f"\n-- items (largest volume first; showing {min(a.top, len(res))} of {len(res)}) --")
    print(res.sort_values("total", ascending=False).head(a.top).round(3).to_string(index=False))
    if a.out:
        res.to_csv(a.out, index=False)
        print(f"\nfull table -> {a.out}")


if __name__ == "__main__":
    main()
