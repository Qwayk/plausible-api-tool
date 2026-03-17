# Agent instructions — `skills/` (Plausible)

Scope: `api-tools/qwayk-plausible-safe-agent-cli/skills/`

This folder contains **Agent Skills wrappers** for the Plausible tool. These are **text-only** wrappers that tell an agent runtime how to use the CLI safely.

## Non-negotiables

- **No secrets**: never include API keys, tokens, cookies, or Authorization headers in any skill docs.
- **No free-form shell**: skills must only use the Qwayk CLI (`plausible-api-tool`) and must not instruct running arbitrary shell commands.
- **Dry-run by default**: never write analytics (Events API) unless the user explicitly approves applying.
- **Explicit apply gates for writes**:
  - Events API `event send` is **irreversible** and requires `--apply --yes --ack-irreversible`.
- **Plan → review → apply → verify → receipt**: preserve this loop; do not skip verification/receipt steps.

## Current skills

- `plausible-api-safe-cli/` → `SKILL.md`

## Living knowledge

If the Plausible CLI changes safety gates, output schema, or command names, update:
- `skills/plausible-api-safe-cli/SKILL.md`
- `docs/skills_wrappers.md`

