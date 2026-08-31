---
name: lifeyoda-horizon
description: Show the LifeYoda long-horizon planning view from the private horizon config without writing changes.
---

# LifeYoda Horizon

Use this skill when the user asks for the LifeYoda horizon view, critical path, track expansion, or week advance view.

Read these packaged files relative to this skill:

- `../../config/public.defaults.json`
- `../../config/horizon.schema.json`
- `../../docs/horizon-layer.md`
- `../../private.example/horizon.example.json` only as a shape reference when private config is missing

Resolve private horizon config in this order:

1. `$LIFEYODA_CONFIG`
2. `~/.lifeyoda/horizon.json`
3. `private/horizon.json` only when running from a LifeYoda source checkout

This workflow is read-only. Do not write to Notion, calendars, source repos, or the horizon config.

Supported modes match the source command: no argument for the backward view, `--track <id>` for one track, and `--week` for this week's advance. Render every date as `YYYY-MM-DD`.
