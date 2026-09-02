# Model selection per scope

Pick the cheapest model that can still do the unit's job well — not the strongest one available. Judge each unit on ambiguity and stakes, not on how big it sounds.

- **Haiku** — mechanical, low-ambiguity, well-specified work: boilerplate, renames, formatting/lint fixes, simple CRUD, doc/README edits, running a known command and reporting the result, straightforward data lookups. If a unit's prompt could be a checklist a junior could follow without judgment calls, it's Haiku.

- **Sonnet (default)** — most engineering work: implementing a feature against a clear spec, routine debugging, standard refactors, code review of typical changes, writing tests. Use this whenever a unit doesn't clearly fall to either edge.

- **Opus** — high-ambiguity or high-stakes work: architecture/design decisions, cross-cutting refactors touching many subsystems, security-sensitive code, anything requiring multi-step judgment calls where a wrong turn is expensive to unwind, or synthesizing a plan from conflicting constraints.

When unsure between two tiers, prefer the cheaper one for a first pass and note in the plan that it may need escalation — don't default everything to Opus "to be safe"; that defeats the point of scoping work into units in the first place.

## Local and other-provider models

The Agent tool only spawns Claude models (`sonnet`/`opus`/`haiku`/`fable`) — it has no slot for a local or third-party model. A unit assigned to one of those doesn't go through the Agent tool at all; it runs as a direct call, driven by Bash/PowerShell (or `WebFetch` for a hosted API), and its output is read back and folded into the plan same as any sub-agent's. Say so explicitly in the plan table's Agent type column (e.g. "external: ollama/qwen2.5-coder") so the approval step shows it's a different execution path, not a Claude tier.

Reach for a non-Claude model only when the unit has a concrete reason to leave Claude — the user names a specific model, the work must run offline/air-gapped, or it's cheap/bulk/well-specified work better suited to whatever's already running locally. Otherwise default to the Claude tiers above; don't split work across providers just because more than one is available.

Common shapes, in order of how often they come up:

- **Ollama** (most common local case): `ollama run <model> "<prompt>"` for a single-shot unit, or POST to `http://localhost:11434/api/generate` for anything needing structured output. Check `ollama list` first — don't assume a model is pulled.
- **OpenAI-compatible local server** (LM Studio, vLLM, llama.cpp server): POST to its `/v1/chat/completions` endpoint (usually `http://localhost:1234` or `:8000`) with a normal chat-completions body.
- **Hosted third-party API** (OpenAI, Gemini, a team's internal endpoint): use `WebFetch`, and check for the expected API-key env var before assuming the call will authenticate — if it's missing, surface that in the plan rather than spawning a call that will just fail.

Before approval, confirm the target is actually reachable (the process is running, the endpoint answers) — a unit routed to an unreachable local model is worse than not scoping it out at all.
