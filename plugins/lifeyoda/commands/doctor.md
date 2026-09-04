---
description: Check that LifeYoda will work. Validates config, Notion database shape, calendar access, repo paths, and enabled sources. Writes nothing.
argument-hint: "[nothing]"
disable-model-invocation: true
---

# /lifeyoda:doctor

Report whether LifeYoda works and where it fails first. This flow writes nothing.

Read `${CLAUDE_PLUGIN_ROOT}/workflows/doctor.md` and follow it exactly. Its `## Inputs`
section lists every other file this flow needs — read those first, before doing anything
else. Do not substitute this file's summary for the workflow.

If this command has been migrated into a Codex skill, read `../../workflows/doctor.md`
relative to the migrated skill instead, and resolve its Inputs the same way.

Never report a check that could not run as a pass: an unavailable connector yields `UNKNOWN`, never `OK`.
