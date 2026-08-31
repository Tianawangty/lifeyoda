---
name: lifeyoda-daily
description: Run the LifeYoda morning brief and draft day plan workflow when the user asks for LifeYoda daily planning or the daily brief.
---

# LifeYoda Daily

Use this skill for the LifeYoda morning brief and draft day plan flow.

Read these packaged files relative to this skill:

- `../../workflows/morning-brief-and-plan.md`
- `../../config/public.defaults.json`
- `../../private.example/local.example.json` only as a shape reference when private config is missing

Resolve private config in this order:

1. `$LIFEYODA_CONFIG`
2. `~/.lifeyoda/local.json`
3. `private/local.json` only when running from a LifeYoda source checkout

The workflow is read-only. Do not write to Notion, calendars, Slack, Gmail, GitHub, or checklist sources. If no private config resolves, say that LifeYoda private config is missing and stop; do not invent sources.

Target date is today in the configured timezone unless the user names a date.

Output the workflow's `# Morning Brief` and `# Draft Day Plan` sections. Ask the one required question round between them. When the user confirms the draft, tell them to run the apply-planner flow in the same conversation.
