---
description: Write a confirmed Draft Day Plan to the Notion Daily Plan row and mirror its blocks to the planning calendar.
argument-hint: "[date, defaults to the draft's date | --demo [--demo-date YYYY-MM-DD]]"
disable-model-invocation: true
---

# /lifeyoda:apply-planner

Write a confirmed Draft Day Plan. Run it only after the user has confirmed one.

Read `${CLAUDE_PLUGIN_ROOT}/workflows/apply-daily-plan.md` and follow it exactly. Its `## Inputs`
section lists every other file this flow needs — read those first, before doing anything
else. Do not substitute this file's summary for the workflow.

If this command has been migrated into a Codex skill, read `../../workflows/apply-daily-plan.md`
relative to the migrated skill instead, and resolve its Inputs the same way.

`$ARGUMENTS` may name a date; it defaults to the draft's own date.

Never reconstruct a plan from memory. If no confirmed draft exists in this conversation, stop and say so.
