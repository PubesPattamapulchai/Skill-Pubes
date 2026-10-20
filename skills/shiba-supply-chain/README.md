# shiba-supply-chain

A [Claude Code](https://claude.com/claude-code) skill that reads a supply-chain dataset (CSV/Excel/ERP export, SAP-style or plain columns) and explains it like a senior supply-chain analyst.

1. **Profiles** every column — type, nulls, uniqueness, ranges, samples.
2. **Finds the grain** — what one row is and which columns make it unique.
3. **Decodes each column** — likely meaning, the evidence, and a confidence level; low-confidence guesses become questions for you, not facts.
4. **Judges business use** — can this data drive safety stock, forecasting, ABC/XYZ, supplier performance, spend, inventory health? Usable now, usable after a named fix, or not usable.
5. **Hands off** to [`shiba-supply-chain-stats`](../shiba-supply-chain-stats) with proposed targets and groupings.

`references/field-dictionary.md` holds SAP (MATNR, WERKS, LIFNR, MATKL, BWART, PLIFZ, ...) and generic ERP column hints.

## Install

Part of the [Skill-Pubes](../..) collection — see the [top-level README](../../README.md). Short version:

```sh
cp -r Skill-Pubes/skills/shiba-supply-chain "$HOME/.claude/skills/shiba-supply-chain"
```

## Use

Type `/shiba-supply-chain` and point it at a file, or just share supply-chain data and ask what it means.

## Requires

- Python with `pandas` (and `openpyxl` for Excel).
- Optionally [`shiba-supply-chain-stats`](../shiba-supply-chain-stats) for the follow-up statistics.

## License

MIT — see [LICENSE](../../LICENSE).
