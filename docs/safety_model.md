# Safety model

Rules:
- Dry-run by default; no writes unless `--apply`.
- Verify after write when possible (Plausible Events API does not offer a reliable read-back).
- Refuse when unsure; do not guess.
- Events write requires `--apply`, `--yes`, and `--ack-irreversible` (it pollutes analytics and is not undoable).
- Refuse sending likely PII in event props (e.g. emails/tokens).
- Never log secrets.

## Events API verification note

Plausible's Events API does not provide a direct “read back this exact event” endpoint.
This tool supports a **best-effort** verification mode (`event send --verify`) which works best when
you send to a unique, never-used URL path.
