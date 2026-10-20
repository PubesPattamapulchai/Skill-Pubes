# Skill-Pubes

A small collection of [Claude Code](https://claude.com/claude-code) skills.

| Skill | Use it to... |
|---|---|
| [`shiba-kickoff`](skills/shiba-kickoff) | Turn "start working on this" into a set of scoped, right-sized sub-agents — survey, grill for scope, plan, then build, test, and code-review it with superpowers. |
| [`shiba-build-loop`](skills/shiba-build-loop) | Build a feature or fix a bug in small, independently-verified increments — plan → implement → test → fix, one step at a time, never batched. |
| [`shiba-build-loop-ui`](skills/shiba-build-loop-ui) | `shiba-build-loop`'s discipline for web UI work — every increment is also verified live in a real browser, not just by automated tests. |
| [`shiba-thorough-tests`](skills/shiba-thorough-tests) | Write or review tests that actually catch bugs — happy path, edge cases, invalid input, regressions, no tautological assertions. |
| [`shiba-root-cause-fix`](skills/shiba-root-cause-fix) | Fix a red test/check/bug by root cause instead of guess-patching, with a hard stop before thrashing. |
| [`shiba-ui-verify`](skills/shiba-ui-verify) | Verify a web UI actually works by driving it in a real browser — render, interaction result, console, network, viewport. |
| [`shiba-ui-theme`](skills/shiba-ui-theme) | Design or restyle a UI so its look comes from what the project is actually about — vivid and expressive for an anime project, pitch-toned and kinetic for a football one — instead of defaulting to generic style. |
| [`shiba-beat-baseline`](skills/shiba-beat-baseline) | Beat a known baseline (DL/ML or not) using only fixed, on-hand data — read what's already been tried, score candidate methods by expected uplift vs. effort/risk, rank worth-it vs. not, pilot the best before a full rollout. |
| [`shiba-supply-chain`](skills/shiba-supply-chain) | Read a supply-chain dataset (SAP-style or plain columns): what each column likely means, what one row is, and whether it's usable for planning, inventory, or procurement decisions. |
| [`shiba-supply-chain-stats`](skills/shiba-supply-chain-stats) | Descriptive stats (mean, SD, CV, outliers, skew) of LT, demand, etc., overall and by month/quarter/year/weekday/matgrp/plant, with a business reading. |

`shiba-build-loop`/`shiba-build-loop-ui` are thin orchestrators over the other three — each of `shiba-thorough-tests`, `shiba-root-cause-fix`, and `shiba-ui-verify` is scoped to do one thing and works fine invoked on its own, outside the loop.

Each skill is self-contained in its own directory (`SKILL.md` plus, where present, `references/`) and can be installed independently.

## Install

Clone the repo once, then run the install script to copy every skill into your global skills directory:

```sh
git clone https://github.com/PubesPattamapulchai/Skill-Pubes.git
cd Skill-Pubes
./install.sh              # global, all skills — macOS/Linux/Git Bash
# or on Windows PowerShell:
.\install.ps1
```

Flags: `--project`/`-Project` installs into `.claude/skills` (this project only) instead of global; `--link`/`-Link` symlinks instead of copying, so `git pull` updates apply without reinstalling; `--dest DIR`/`-Dest DIR` installs somewhere else. Re-run anytime to sync after pulling changes.

To install only specific skills instead, copy (or symlink) them individually:

```sh
git clone https://github.com/PubesPattamapulchai/Skill-Pubes.git

# global — available in every project
cp -r Skill-Pubes/skills/<skill-name> "$HOME/.claude/skills/<skill-name>"

# project-scoped instead
cp -r Skill-Pubes/skills/<skill-name> .claude/skills/<skill-name>
```

On Windows, `$HOME` is `%USERPROFILE%`. A symlink works the same as a copy and picks up updates on `git pull`:

```sh
ln -s "$(pwd)/Skill-Pubes/skills/<skill-name>" "$HOME/.claude/skills/<skill-name>"
```

See each skill's own `README.md` for what it needs beyond this (some depend on another skill being installed too).

## License

MIT — see [LICENSE](LICENSE).
