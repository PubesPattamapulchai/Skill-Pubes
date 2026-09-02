# kickoff

A [Claude Code](https://claude.com/claude-code) skill that turns "start working on this" into a set of scoped, right-sized sub-agents.

1. **Surveys the project** — README/CLAUDE.md/AGENTS.md, manifest files, existing `.claude/agents`/`.claude/skills`, git history, and a `graphify-out/graph.json` if one exists.
2. **Grills you for scope** wherever the survey leaves gaps — nothing here to build on, or what's here doesn't say what to build next.
3. **Drafts a plan**: the settled scope broken into units, each with a recommended model (cheapest Claude tier that fits, or a local/other-provider model when there's a concrete reason to leave Claude) and any skills the unit should be pointed at.
4. **Waits for your approval** on the plan — nothing gets spawned until you confirm.
5. **Spawns** each approved unit — via the Agent tool for a Claude tier, or as a direct local/API call for a non-Claude model.

## Install

Clone straight into your skills directory so it's available in every project:

```sh
git clone https://github.com/PubesPattamapulchai/kickoff-skill.git "$HOME/.claude/skills/kickoff"
```

(On Windows: `%USERPROFILE%\.claude\skills\kickoff`.)

To scope it to one project instead, clone into `.claude/skills/kickoff` at the repo root.

## Use

Type `/kickoff`, or just start describing work you want kicked off — the skill's description is written to trigger on its own for "start new/unclear work," "kick off/bootstrap a project," and "split this into parallel agents."

## Requires

- The `grilling` skill for Step 2's interview — ships in the [`mattpocock-skills`](https://github.com/mattpocock/skills) plugin.
- Optionally, a `graphify` skill for Step 1, if the project already has a `graphify-out/` knowledge graph.

## License

MIT — see [LICENSE](LICENSE).
