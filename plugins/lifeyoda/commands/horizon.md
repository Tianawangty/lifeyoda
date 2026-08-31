---
description: Long-horizon view. Counts back from the terminal goal through hard deadlines and track milestones. Reads config only, writes nothing.
argument-hint: "[nothing | --track <id> | --week]"
disable-model-invocation: true
---

# /lifeyoda:horizon

Show where the LifeYoda long horizon stands. This command writes nothing.

1. Read `${CLAUDE_PLUGIN_ROOT}/config/public.defaults.json` for toolkit defaults, including `horizon.lookaheadDays` and `horizon.confidenceLevels`. If this command has been migrated into a Codex skill, read `../../../config/public.defaults.json` relative to the migrated skill instead.
2. Read `${CLAUDE_PLUGIN_ROOT}/config/horizon.schema.json` as the authority on the private horizon file's shape. If this command has been migrated into a Codex skill, read `../../../config/horizon.schema.json` relative to the migrated skill instead.
3. Resolve private horizon config in this order:
   - `$LIFEYODA_CONFIG`
   - `~/.lifeyoda/horizon.json`
   - `private/horizon.json` only when running from a LifeYoda source checkout
4. If no private horizon config resolves, say so and stop. Point at `${CLAUDE_PLUGIN_ROOT}/private.example/horizon.example.json` as the template to copy. Do not invent a goal, a deadline, or a milestone.

Today is the current date in the daily config's timezone unless `$ARGUMENTS` names a date.

Follow the modes and output discipline in the packaged horizon command workflow: no argument for backward view, `--track <id>` for one track, and `--week` for this week's advance. Render every date as `YYYY-MM-DD`.
