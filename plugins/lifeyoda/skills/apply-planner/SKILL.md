---
name: lifeyoda-apply-planner
description: Apply a confirmed LifeYoda Draft Day Plan to the configured Daily Plan destination and planning calendar.
---

# LifeYoda Apply Planner

Use this skill only when the user asks to apply a confirmed LifeYoda Draft Day Plan.

Read these packaged files relative to this skill:

- `../../workflows/apply-daily-plan.md`
- `../../config/public.defaults.json`
- `../../templates/daily-plan-page.md`

Resolve private config in this order:

1. `$LIFEYODA_CONFIG`
2. `~/.lifeyoda/local.json`
3. `private/local.json` only when running from a LifeYoda source checkout

Never run this workflow without an explicit confirmed draft in the current conversation. If no confirmed draft exists, stop and say so; do not reconstruct a plan from memory.

Write only the destinations allowed by the workflow: one Daily Plan row and confirmed timed blocks on the configured planning calendar. Do not create a Daily Journal, write other calendars, write task trackers, or add helper properties to Notion databases.

Return a concise apply report with created, updated, skipped, unavailable, and collision items.
