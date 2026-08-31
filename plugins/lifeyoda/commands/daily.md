---
description: Morning brief and draft day plan. Reads calendars, Notion checklists, and the active repo. Writes nothing.
argument-hint: "[optional: focus area, or a date like 2026-08-20]"
disable-model-invocation: true
---

# /lifeyoda:daily

Run the LifeYoda morning-brief-and-plan workflow. This command writes nothing.

1. Read `${CLAUDE_PLUGIN_ROOT}/workflows/morning-brief-and-plan.md` and follow it exactly. If this command has been migrated into a Codex skill, read `../../../workflows/morning-brief-and-plan.md` relative to the migrated skill instead.
2. Read `${CLAUDE_PLUGIN_ROOT}/config/public.defaults.json` for toolkit defaults.
3. Resolve private config in this order:
   - `$LIFEYODA_CONFIG`
   - `~/.lifeyoda/local.json`
   - `private/local.json` only when running from a LifeYoda source checkout
4. If no private config resolves, say so and stop. Do not invent sources.

Target date is today in the config timezone unless `$ARGUMENTS` names a date.

Output the workflow's `# Morning Brief` and `# Draft Day Plan` sections, with the single question round specified by the workflow. When the user confirms the draft, tell them to run `/lifeyoda:apply-planner`; do not write anything yourself.
