---
name: lifeyoda-apply-planner
description: Apply a confirmed LifeYoda Draft Day Plan to the configured Daily Plan destination and planning calendar.
---

# LifeYoda Apply Planner

Use this skill when the user confirms a Draft Day Plan and asks for it to be written.

Write a confirmed Draft Day Plan. Run it only after the user has confirmed one.

Read `../../workflows/apply-daily-plan.md` and follow it exactly. Its `## Inputs` section lists every
other file this flow needs — read those first, before doing anything else. Do not substitute
this file's summary for the workflow.

`the request` may name a date; it defaults to the draft's own date.

Never reconstruct a plan from memory. If no confirmed draft exists in this conversation, stop and say so.
