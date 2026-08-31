# Daily Journal Page Template

Part of the public toolkit. Not user-specific configuration.

## Row Properties

`Day` (title):
- Same format as the matching Daily Plan title, `Wed, June 17, 2026`.

`Date` (date):
- ISO `YYYY-MM-DD`, the day being journaled. Unlike the plan's `Date`, this one is writable and must be correct even when the journal is written late.

`Focus Hours` (number):
- Derived per `focusHours.strategy`: worklog calendars, else reconstructed from the day's commits, else asked.
- Always show the derivation before writing. Say which strategy produced it.

`Projects Touched` (multi-select):
- From `sources.projectMapping` for repos with commits today, plus non-repo categories judged from the day's content.
- Only options that already exist in the database. Never invent one.

`☑️ Daily Plan` (relation):
- Required. The journal must not exist without it.

Icon:
- `✅` when every planned checklist item is complete.
- `📓` when completion is partial.

Matching Daily Plan `Status`:
- `Done` when complete, `Partial` when partial.

## Page Body

## What got done

{{what_got_done}}

## Not done → carry forward

{{not_done_carry_forward}}

Written for tomorrow's morning brief, which reads this section. Each item must stand on its own a day later.

## Extra bonus

{{extra_bonus}}

Unplanned work that actually happened. If the user did not mention any, ask before writing the journal — never conclude there was none.

## Tomorrow's seeds ({{tomorrow_date}})

{{tomorrows_seeds}}

## Time-on-task

{{time_on_task}}

States the hours and where the number came from. Flag any gap between logged time and observed work rather than smoothing it over.
