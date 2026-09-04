---
name: lifeyoda-horizon
description: Show the LifeYoda long-horizon planning view from the private horizon config without writing changes.
---

# LifeYoda Horizon

Use this skill when the user asks for the horizon view, the critical path, or one track expanded.

Report where the long horizon stands. This flow writes nothing.

Read `../../workflows/horizon.md` and follow it exactly. Its `## Inputs` section lists every
other file this flow needs — read those first, before doing anything else. Do not substitute
this file's summary for the workflow.

Today is the current date in the daily config's timezone unless `the request` names one.

Building the chain belongs to the setup flow. This flow reports; it does not derive milestones.
