# Configuration

This directory separates public toolkit configuration from private user configuration.

## Public Files

- `public.defaults.json` defines generic defaults that are safe to commit.
- `local.schema.json` defines the expected shape of private config files.
- `private.example/` contains placeholder examples with no real personal IDs.

## Private Files

All real user-specific files must live under:

```text
private/
```

This folder is excluded by `.gitignore`.

Recommended private files:

- `private/local.json`
- `private/state.json`
- `private/notion.json`
- `private/sources.json`

Do not commit real Notion IDs, Slack IDs, Gmail labels, calendar IDs, course sources, active repo choices, or personal workflow state.

