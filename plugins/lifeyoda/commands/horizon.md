---
description: Long-horizon view. Counts back from the terminal goal through hard deadlines and track milestones, and reports defects in the chain. Reads config only, writes nothing.
argument-hint: "[nothing | --track <id> [--evidence] | --demo [--demo-date YYYY-MM-DD]]"
disable-model-invocation: true
---

# /lifeyoda:horizon

Report where the long horizon stands. This flow writes nothing.

Read `${CLAUDE_PLUGIN_ROOT}/workflows/horizon.md` and follow it exactly. Its `## Inputs`
section lists every other file this flow needs — read those first, before doing anything
else. Do not substitute this file's summary for the workflow.

If this command has been migrated into a Codex skill, read `../../workflows/horizon.md`
relative to the migrated skill instead, and resolve its Inputs the same way.

Today is the current date in the daily config's timezone unless `$ARGUMENTS` names one.

Building the chain belongs to `/lifeyoda:setup`. This flow reports; it does not derive milestones.
