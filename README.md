# Plausible Analytics tool for AI agents

This is a public Qwayk proof repo.

It gives AI agents a safer way to work with Plausible Analytics.
This repo matters because it shows the full Qwayk safety model, not just read-only access.

## What this tool is for

Use this when you want an agent to help with Plausible work like:
- traffic reports
- top pages and sources
- goal reporting
- event workflows that require explicit approval

## Why this repo is public

This repo shows the Qwayk model clearly:
- plan first
- writes require explicit approval
- verify after apply
- keep a receipt

If you want to understand Qwayk fast, this is one of the best repos to read.

## For non-technical users

Start here:
- `docs/use_cases.md`
- `docs/onboarding.md`
- `docs/safety_model.md`

Example things to ask your agent:
- “Give me a weekly traffic report.”
- “Show me top pages and traffic sources for the last 30 days.”
- “Validate this query before running it.”
- “Send a test event only if I approve it.”

## For technical users

Start here:
- `docs/quickstart.md`
- `docs/command_reference.md`

Minimal examples:

```bash
plausible-api-tool --version
plausible-api-tool --env-file .env auth check
```

## Skills and wrappers

This tool ships with a skill wrapper for agent runtimes that support skills:
- `skills/plausible-api-safe-cli/SKILL.md`
- `docs/skills_wrappers.md`

## Qwayk

- Start here: `https://github.com/Qwayk/start-here`
- Sponsor Qwayk: `https://github.com/sponsors/Qwayk`
