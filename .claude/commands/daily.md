---
description: Morning brief and draft day plan. Reads calendars, Notion checklists, and the active repo. Writes nothing.
argument-hint: "[optional: focus area, or a date like 2026-08-20]"
---

# /daily

Run the morning-brief-and-plan workflow. **This command writes nothing** — not to Notion, not to any calendar.

1. Read `workflows/morning-brief-and-plan.md` and follow it exactly.
2. Read `config/public.defaults.json` for toolkit defaults.
3. Resolve private config in this order, first hit wins:
   - `$LIFEYODA_CONFIG`
   - `~/.lifeyoda/local.json`
   - `private/local.json`
4. If no private config resolves, say so and stop. Do not invent sources.
5. Run the workflow's Config Health check before reading any source, and lead the brief with its result. An unset `$VAR`, a path that does not exist, and a path that is not a git repository are equivalent failures — name each one rather than reading it as a repo with no commits.

Target date is today in the config timezone unless `$ARGUMENTS` names a date.

Output exactly two sections — `# Morning Brief` and `# Draft Day Plan` — with a single round of questions between them, as specified in the workflow. When the user confirms the draft, tell them to run `/apply-planner`; do not write anything yourself.
