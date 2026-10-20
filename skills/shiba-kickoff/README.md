# shiba-kickoff

A [Claude Code](https://claude.com/claude-code) skill that turns "start working on this" into a set of scoped, right-sized sub-agents.

1. **Surveys the project** — README/CLAUDE.md/AGENTS.md, manifest files, existing `.claude/agents`/`.claude/skills`, git history, and a `graphify-out/graph.json` if one exists.
2. **Grills you for scope** wherever the survey leaves gaps — nothing here to build on, or what's here doesn't say what to build next.
3. **Drafts a plan**: the settled scope broken into units, each with a recommended model (cheapest Claude tier that fits, or a local/other-provider model when there's a concrete reason to leave Claude) and any skills the unit should be pointed at.
4. **Builds it** — after a grilling session it proceeds without another approval (if the survey alone gave the task, it waits for your confirmation first). Uses `superpowers` `writing-plans` → `subagent-driven-development` with test-first implementers.
5. **Tests it** — full suite and build via `verification-before-completion`, plus a live browser pass for web UIs.
6. **Code-reviews it** — `requesting-code-review` / `receiving-code-review`, up to 2 rounds, then hands the branch to `finishing-a-development-branch` so you pick merge/PR.

## Install

This skill lives in the [Skill-Pubes](../..) collection — see the [top-level README](../../README.md) for the general install steps. Short version:

```sh
git clone https://github.com/PubesPattamapulchai/Skill-Pubes.git
cp -r Skill-Pubes/skills/shiba-kickoff "$HOME/.claude/skills/shiba-kickoff"
```

(On Windows: `%USERPROFILE%\.claude\skills\shiba-kickoff`.) To scope it to one project instead, copy into `.claude/skills/shiba-kickoff` at that project's repo root.

## Use

Type `/shiba-kickoff`, or just start describing work you want kicked off — the skill's description is written to trigger on its own for "start new/unclear work," "kick off/bootstrap a project," and "split this into parallel agents."

## Requires

- The `grilling` skill for Step 2's interview — ships in the [`mattpocock-skills`](https://github.com/mattpocock/skills) plugin.
- The [`superpowers`](https://github.com/obra/superpowers) plugin for Steps 5-8 (falls back to `shiba-build-loop` and `code-review` without it).
- Optionally, a `graphify` skill for Step 1, if the project already has a `graphify-out/` knowledge graph.

## License

MIT — see [LICENSE](../../LICENSE).
