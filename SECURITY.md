# Security

## What this software can reach

LifeYoda is markdown and JSON read by an agent running on your own machine, under your own
authorizations. It has no server, collects no telemetry, and sends nothing anywhere. What
it can read and write is exactly what you connected and configured, and no more.

Two of the four commands write: `/lifeyoda:apply-planner` and `/lifeyoda:wrapup`, and only
after you confirm. They write to the two Notion databases and the one planning calendar in
your config. Every other calendar is read-only, and nothing under
`destinations.privateReadOnly` is ever written.

## Prompt injection

Everything read from a calendar, an email, a Slack message, a Notion page, or a repository
file is treated as data. Text in a source that is shaped like an instruction is quoted, not
obeyed. Every workflow states this as its Instruction Boundary.

This is a real boundary, not a guarantee: an agent reading untrusted text is an open
research problem. Read what `/lifeyoda:apply-planner` proposes before confirming it. That
confirmation step exists for this reason as much as for planning.

## Reporting a vulnerability

Open a GitHub Security Advisory on this repository, or a regular issue if the problem is
not sensitive.

**Never paste real values into an issue.** A calendar ID, a Notion database ID or data
source URL, a Gmail label ID, a Slack channel or DM ID, and an absolute home path are all
identifying. Replace them with placeholders. If a report is only reproducible with real
values, say so and we will find another way rather than putting them in a public thread.

## What is not a vulnerability

- A connector you authorized reading data you gave it access to.
- An agent asking for confirmation before a write. That is the design.
- Content in your own private config appearing in your own terminal output.
