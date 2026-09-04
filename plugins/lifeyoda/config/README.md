# Configuration

This directory separates public toolkit configuration from private user configuration.

## Public Files

- `public.defaults.json` defines generic defaults that are safe to commit.
- `local.schema.json` defines the expected shape of private config files.
- `private.example/` contains placeholder examples with no real personal IDs.

## Private Files

All real user-specific files live in one directory, resolved in this order, first hit wins:

```text
$LIFEYODA_CONFIG   # explicit override; a directory, like the other two
~/.lifeyoda/       # a real directory, or a symlink to a folder you back up
private/           # source checkout only, and only when that is the working directory
```

`private/**` is excluded by `.gitignore`.

The files that directory holds:

- `local.json` — the private config this schema describes
- `horizon.json` — the long-horizon goal, deadlines, and milestones, if you use `/horizon`
- `NOTES.md` — optional free-form notes, read by nothing

Do not commit real Notion IDs, Slack IDs, Gmail labels, calendar IDs, course sources, active repo choices, or personal workflow state.
