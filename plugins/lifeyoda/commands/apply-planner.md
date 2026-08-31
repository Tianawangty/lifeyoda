---
description: Write a confirmed Draft Day Plan to the Notion Daily Plan row and mirror its blocks to the planning calendar.
argument-hint: "[optional: date, defaults to the draft's date]"
disable-model-invocation: true
---

# /lifeyoda:apply-planner

Run the LifeYoda apply-daily-plan workflow. Only run after the user has confirmed a Draft Day Plan.

1. Read `${CLAUDE_PLUGIN_ROOT}/workflows/apply-daily-plan.md` and follow it exactly. If this command has been migrated into a Codex skill, read `../../../workflows/apply-daily-plan.md` relative to the migrated skill instead.
2. Read `${CLAUDE_PLUGIN_ROOT}/config/public.defaults.json`.
3. Resolve private config in this order:
   - `$LIFEYODA_CONFIG`
   - `~/.lifeyoda/local.json`
   - `private/local.json` only when running from a LifeYoda source checkout
4. If there is no confirmed draft in this conversation, stop and say so. Never reconstruct a plan from memory and write it.

Writes exactly two destinations:

- one Notion Daily Plan row for the date
- the confirmed timed blocks on the configured planning calendar

Never write a Daily Journal here. Never write to any calendar other than the configured planning calendar. Never add helper properties to the Notion databases.
