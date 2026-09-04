---
description: Morning brief and draft day plan. Reads calendars, Notion checklists, and the active repo. Writes nothing.
argument-hint: "[focus area | a date like 2026-08-20 | --demo [--demo-date YYYY-MM-DD]]"
disable-model-invocation: true
---

# /lifeyoda:daily

Produce the Morning Brief and the Draft Day Plan. This flow writes nothing.

Read `${CLAUDE_PLUGIN_ROOT}/workflows/morning-brief-and-plan.md` and follow it exactly. Its `## Inputs`
section lists every other file this flow needs — read those first, before doing anything
else. Do not substitute this file's summary for the workflow.

If this command has been migrated into a Codex skill, read `../../workflows/morning-brief-and-plan.md`
relative to the migrated skill instead, and resolve its Inputs the same way.

Target date is today in the config timezone unless `$ARGUMENTS` names one.

When the user confirms the draft, tell them to run `/lifeyoda:apply-planner`. Do not write anything yourself.
