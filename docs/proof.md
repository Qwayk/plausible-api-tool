# Proof pack

Last verified (UTC): 2026-02-03

Note: you don’t need to run these commands yourself. They exist so you (or your reviewer/agent) can audit behavior and prove what happened.

## Smoke commands (safe)

All commands below are safe to run locally; they do not print secrets.

- Install (minimal): `python3 -m venv .venv && . .venv/bin/activate && .venv/bin/python -m pip install -e .`
- Optional (dev extras): `.venv/bin/python -m pip install -e '.[dev]'`
- Version (JSON): `python3 -m plausible_api_tool --output json --version`
- Config/auth sanity (requires valid env file): `python3 -m plausible_api_tool --output json --env-file .env auth check`
- Stats query from file (read-only): `python3 -m plausible_api_tool --output json --env-file .env stats validate --file examples/goals_list_query.json`
- Sites list (read-only; requires valid env file): `python3 -m plausible_api_tool --output json --env-file .env site list`
- Events dry-run plan (no write; requires valid env file): `python3 -m plausible_api_tool --output json --env-file .env event send --name test_event --url https://example.com/ --referrer https://example.com/from --revenue-currency USD --revenue-amount 9.99`

## What can go wrong

- **Auth blocked** (Stats API): missing/invalid `PLAUSIBLE_API_KEY` or wrong `PLAUSIBLE_BASE_URL`.
- **Query rejected**: invalid Stats API v2 query JSON shape (use `stats validate`).
- **Event refused**: missing `--apply`, missing `--yes`, missing `--ack-irreversible`, domain/host mismatch, or props that look like PII.
- **Sites write refused**: missing `--apply`/`--yes`, or missing `--ack-irreversible` for destructive operations.
- **Sites permission errors**: some destructive endpoints require an owner API key for the site.

## Proof artifacts (committed, redacted)

- Example outputs: `docs/examples/outputs/`
- Sites example output (synthetic): `docs/examples/outputs/site_list_ok.synthetic.json`
- Example plan: `docs/examples/plan.example.json`
- Example receipt: `docs/examples/receipt.example.json`
