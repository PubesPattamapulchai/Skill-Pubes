# Skill-Pubes

A small collection of [Claude Code](https://claude.com/claude-code) skills.

| Skill | Use it to... |
|---|---|
| [`kickoff`](skills/kickoff) | Turn "start working on this" into a set of scoped, right-sized sub-agents — survey, grill for scope, plan, get approval, spawn. |
| [`build-loop`](skills/build-loop) | Build a feature or fix a bug in small, independently-verified increments — plan → implement → test → fix, one step at a time, never batched. |
| [`build-loop-ui`](skills/build-loop-ui) | `build-loop`'s discipline for web UI work — every increment is also verified live in a real browser, not just by automated tests. |
| [`thorough-tests`](skills/thorough-tests) | Write or review tests that actually catch bugs — happy path, edge cases, invalid input, regressions, no tautological assertions. |
| [`root-cause-fix`](skills/root-cause-fix) | Fix a red test/check/bug by root cause instead of guess-patching, with a hard stop before thrashing. |
| [`ui-verify`](skills/ui-verify) | Verify a web UI actually works by driving it in a real browser — render, interaction result, console, network, viewport. |
| [`beat-baseline`](skills/beat-baseline) | Beat a known baseline (DL/ML or not) using only fixed, on-hand data — read what's already been tried, score candidate methods by expected uplift vs. effort/risk, rank worth-it vs. not, pilot the best before a full rollout. |

`build-loop`/`build-loop-ui` are thin orchestrators over the other three — each of `thorough-tests`, `root-cause-fix`, and `ui-verify` is scoped to do one thing and works fine invoked on its own, outside the loop.

Each skill is self-contained in its own directory (`SKILL.md` plus, where present, `references/`) and can be installed independently.

## Install

Clone the repo once, then copy (or symlink) the skill(s) you want into your skills directory:

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
