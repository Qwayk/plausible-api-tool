# Agent Skills wrappers

This tool ships with an **Agent Skills wrapper**: a small, text-only “how to run this CLI safely” package you can copy into an agent runtime’s skills directory.

## Where it lives in this repo

- Skill: `skills/plausible-api-safe-cli/SKILL.md`
- Skills scope rules: `skills/AGENTS.md`

## How to install (example: Codex)

Copy (or symlink) the whole folder:

- From: `api-tools/qwayk-plausible-safe-agent-cli/skills/plausible-api-safe-cli/`
- To (example): `~/.codex/skills/plausible-api-safe-cli/`

Then refresh your runtime’s skills list (runtime-specific).

## Safety model recap

The wrapper enforces the standard Qwayk safety flow:

1) Discover (read-only)
2) Dry-run plan (when applicable)
3) Human review (you or a reviewer agent)
4) Apply with explicit flags
5) Verify and save receipts / ledgers

For Plausible specifically:

- Stats API (`stats ...`) is **read-only**.
- Events API (`event send`) is an **irreversible write**. The apply path requires **all** flags: `--apply --yes --ack-irreversible`.
- Prefer saving dry-run plans with `--plan-out` before any write-like action.
- Receipts require an apply step and should be saved with `--receipt-out` (never include secrets).

## Suggested usage prompts (copy/paste)

- “Generate a weekly traffic report: top pages, top sources, and goal conversions. Use `--output json`.”
- “Given these report requirements, propose the smallest Stats queries to answer them and run each query.”
- “Create a dry-run plan for an `event send` (do not apply), then wait for my explicit approval before writing analytics.”

## Setup links

- Auth / API key setup: `authentication.md`
- Quickstart commands: `quickstart.md`
- Full CLI reference: `command_reference.md`
- Safety model details: `safety_model.md`

