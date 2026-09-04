---
description: Set up or update LifeYoda. Creates or adopts the two Notion databases, picks calendars and sources, works backwards from a long-term goal to build a milestone chain, and writes your config. Re-run any time to change one part.
argument-hint: "[nothing]"
disable-model-invocation: true
---

# /lifeyoda:setup

Set up LifeYoda, or change one part of an existing setup.

Read `${CLAUDE_PLUGIN_ROOT}/workflows/setup.md` and follow it exactly. Its `## Inputs`
section lists every other file this flow needs — read those first, before doing anything
else. Do not substitute this file's summary for the workflow.

If this command has been migrated into a Codex skill, read `../../workflows/setup.md`
relative to the migrated skill instead, and resolve its Inputs the same way.

Show the complete config file and get confirmation before writing it. Finish by pointing at `/lifeyoda:doctor`.
