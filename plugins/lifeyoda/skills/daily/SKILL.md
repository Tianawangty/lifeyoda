---
name: lifeyoda-daily
description: Run the LifeYoda morning brief and draft day plan workflow when the user asks for LifeYoda daily planning or the daily brief.
---

# LifeYoda Daily

Use this skill when the user asks for their morning brief, their day plan, or LifeYoda daily planning.

Produce the Morning Brief and the Draft Day Plan. This flow writes nothing.

Read `../../workflows/morning-brief-and-plan.md` and follow it exactly. Its `## Inputs` section lists every
other file this flow needs — read those first, before doing anything else. Do not substitute
this file's summary for the workflow.

Target date is today in the config timezone unless `the request` names one.

When the user confirms the draft, stop and tell them to run the apply-planner flow. Do not run it yourself and do not write anything from this skill, even if the user has already said the draft looks right. Confirming a draft is not the same as asking for it to be written.
