# Agent instructions — `qwayk-plausible-safe-agent-cli/`

Scope: this folder.

## One command to validate

- `python3 -m unittest -q`

## Safety contract (writes)

- Dry-run by default: no writes without `--apply`.
- For any write-like command, require `--yes` for the apply path.
- For **irreversible** actions (Plausible Events API), require `--ack-irreversible` in addition to `--apply --yes`.
- Never print secrets (API keys/tokens, Authorization headers) to stdout/stderr or committed files.
- Plans/receipts must never contain secrets.

## Output contract (automation)

In `--output json` mode, every invocation must print **exactly one JSON object** to stdout:
- Success: `{"ok": true}`
- Refusal (safe no-op): `{"ok": true, "dry_run": true, "refused": true, "reasons": ["Write disabled: pass --apply --yes to proceed."]}`
- Error: `{"ok": false, "error": "Missing required flag", "error_type": "ValidationError"}`

Parse/usage errors must also obey this contract in `--output json` mode.

## Write workflow artifacts (v2)

Write-capable commands may support:
- `--plan-out PATH`: write the computed plan JSON to a file for review (no secrets).
- `--receipt-out PATH`: write the post-apply receipt JSON to a file (no secrets).

## Skills wrapper (shipped)

- Canonical location: `skills/plausible-api-safe-cli/SKILL.md`
- Docs: `docs/skills_wrappers.md`
- If the wrapper changes, keep `docs/skills_wrappers.md` in sync.
