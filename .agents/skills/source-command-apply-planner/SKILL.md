---
name: "source-command-apply-planner"
description: "Write a confirmed Draft Day Plan to the Notion Daily Plan row and mirror its blocks to the planning calendar."
---

# source-command-apply-planner

Use this skill when the user asks to run the migrated source command `apply-planner`.

## Command Template

# /apply-planner

Run the apply-daily-plan workflow. **Only run after the user has confirmed a Draft Day Plan.**

1. Read `workflows/apply-daily-plan.md` and follow it exactly.
2. Read `config/public.defaults.json`, then resolve private config: `$LIFEYODA_CONFIG` → `~/.lifeyoda/local.json` → `private/local.json` when running from a source checkout.
3. If there is no confirmed draft in this conversation, stop and say so. Never reconstruct a plan from memory and write it.

Writes exactly two destinations:

- one Notion Daily Plan row for the date
- the confirmed timed blocks on the configured planning calendar

Never write a Daily Journal here. Never write to any calendar other than the configured planning calendar. Never add helper properties to the Notion databases.
