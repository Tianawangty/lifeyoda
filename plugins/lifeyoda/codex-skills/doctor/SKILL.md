---
name: lifeyoda-doctor
description: Check a LifeYoda installation — validate the private config, the two Notion databases, calendar access, repo paths, and enabled sources. Writes nothing.
---

# LifeYoda Doctor

Use this skill when the user asks whether LifeYoda is set up correctly, or a LifeYoda flow reported something unavailable.

Report whether LifeYoda works and where it fails first. This flow writes nothing.

Read `../../workflows/doctor.md` and follow it exactly. Its `## Inputs` section lists every
other file this flow needs — read those first, before doing anything else. Do not substitute
this file's summary for the workflow.

Never report a check that could not run as a pass: an unavailable connector yields `UNKNOWN`, never `OK`.
