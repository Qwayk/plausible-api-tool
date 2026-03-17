# Project playbook template (Plausible)

Use this file as a starting point for a site-specific “how we use Plausible data to make decisions” playbook.

Keep the real playbook in your project folder (not inside this tool repo).

## First setup

1) Create a Stats API key in Plausible and configure:
- `PLAUSIBLE_BASE_URL`
- `PLAUSIBLE_API_KEY`
- `PLAUSIBLE_SITE_ID=example.com`

2) Smoke test:

```bash
python3 -m plausible_api_tool --env-file .env auth check
```

## Weekly snapshot

```bash
python3 -m plausible_api_tool --env-file .env report weekly --days 7 --limit 50
```

## Goal hygiene

- Make sure the event/goal names you care about are configured as goals in Plausible (Site → Goals).
- When goals are missing, the tool reports them as `missing_goals` in report outputs.

