# Engineering notes

## Issue 47 — API_TOOL_STANDARD v2 alignment

- Added strict JSON output behavior for argparse/usage errors when `--output json` is selected (or defaulted).
- Made `--version` machine-readable in JSON output mode.
- Hardened the Events API workflow with explicit irreversible-write acknowledgement and optional plan/receipt file artifacts.
