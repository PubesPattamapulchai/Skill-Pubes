---
name: shiba-supply-chain
description: Read a supply-chain, procurement, inventory, or logistics dataset (CSV/Excel/ERP export, SAP-style columns like MATNR/WERKS/LIFNR/MATKL, LT, Demand) and explain what each column likely means, what one row represents, and whether the data is usable for business decisions. Use when the user shares or points at supply-chain data, asks "what is this data", "what do these columns mean", "can we use this for planning/inventory/procurement", or before running statistics on it.
---

# Supply Chain Data Reading

Act as a senior supply-chain analyst meeting an unfamiliar export. The job: say what the data *is*, what each column *probably* means, and whether it can drive a decision, while being honest about which parts are inference. A confident wrong meaning for a column (planned LT read as actual LT) poisons every number after it.

Reply in the user's language. Keep codes, column names, and formulas verbatim.

Use `references/field-dictionary.md` for SAP and common ERP column names. Its entries are hypotheses to check against the values, not answers.

## Step 1 — Load and profile

Read the file (all sheets of an Excel file; find the real header row if the top rows are titles). Never print the whole table. Per column get: dtype, null %, unique count, min/max or top values, 3 sample values. Use pandas.

**Completion criterion:** every column has a profile line; row count and any header/footer junk rows are stated.

## Step 2 — Find the grain and the keys

State what one row represents (PO line, goods movement, material-plant-month, delivery, ...). Prove it: test which column combination is unique. Name the time column(s), the item/location/supplier keys, and the quantity and value columns. Say if rows look duplicated, reversed (movement 102/262), or cancelled.

**Completion criterion:** one sentence "one row = X, unique on (A, B, C)", or an explicit "no unique key found; duplicates: N".

## Step 3 — Decode each column

For every column give: likely meaning, **evidence** (name match, value pattern, relation to another column), and **confidence** (high / medium / low). Rules:

- Confidence needs evidence from the values, not only the name. `LT` with values 0-400 and a date pair that reproduces it is high; `LT` with no dates to check it against is medium.
- Pin down the ambiguous families before calling them: **LT** (which two events; planned or actual; calendar or working days), **Demand** (sales vs goods issue vs requirement; stock-outs hide true demand), **date** columns (order, document, posting, delivery), **Qty** (unit, sign), **value** (currency, per-unit vs total, price unit).
- Low-confidence columns go in an "Ask the user" list. Don't present them as fact.

**Completion criterion:** every column covered; every low-confidence one is in the ask list.

## Step 4 — Business usability verdict

Rate the dataset per decision it could support, with the fields it needs and which are present:

| Decision | Needs | Verdict |
|---|---|---|
| Safety stock / reorder point | demand history, LT history (actual), service target | |
| Forecasting | demand per item per period, enough periods | |
| ABC / XYZ classification | value or volume per item, demand variability | |
| Supplier performance (OTIF, LT reliability) | promised vs actual dates, quantities | |
| Spend analysis | value, currency, supplier, category | |
| Inventory health (slow/obsolete) | stock, movements, age | |

Verdict per row: **usable now**, **usable after fixing X**, or **not usable (missing Y)**. Then list data-quality blockers with counts: nulls in key fields, duplicates, reversals not netted, negative or zero quantities, mixed units or currencies, date gaps, impossible dates (delivery before order), LT of 0, sentinel values (a plausible-looking 9999).

**Completion criterion:** every verdict has a stated reason; every blocker has a count.

## Step 5 — Report and hand off

Output, in order:

1. One-paragraph summary: what the data is, grain, period covered, size.
2. Column table: Column | Likely meaning | Evidence | Confidence.
3. Usability verdict table and blockers.
4. **Ask the user**: low-confidence columns and any definition choice that changes numbers.
5. Proposed stats run: target column(s), group-by columns, date column. Then call the Skill tool with `shiba-supply-chain-stats`, unless the user said not to or blockers need fixing first.

**Completion criterion:** a reader who has never seen the file knows what it is and what they can do with it.

## Common mistakes

| Mistake | Fix |
|---|---|
| Reading a column from its name alone | Check values and relations to other columns |
| Treating PLIFZ or master-data "Lead Time" as actual LT | Say planned vs actual; compute actual from dates if present |
| Summing mixed units or currencies | Flag it; group by unit/currency |
| Counting reversals (102/262) or cancelled lines as real demand | Net or exclude, and state which |
| Calling poor data "unusable" without saying what would fix it | Name the fix and the field |
