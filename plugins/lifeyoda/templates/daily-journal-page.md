# Daily Journal Page Template

Part of the public toolkit. Not user-specific configuration.

`docs/page-examples.md` shows this page filled in. Match its density and specificity, not
its wording.

## Row Properties

`Day` (title):
- Same format as the matching Daily Plan title, `Wed, June 17, 2026`.

`Date` (date):
- ISO `YYYY-MM-DD`, the day being journaled. Unlike the plan's `Date`, this one is writable and must be correct even when the journal is written late.

`Focus Hours` (number):
- Derived per `focusHours.strategy`: worklog calendars, else reconstructed from the day's commits, else asked.
- Always show the derivation before writing. Say which strategy produced it.

`Track Hours` (text):
- How the day's `Focus Hours` split across horizon tracks, as `research 3; job 2`.
- Derived from the worklog calendar: every block carries a `[project]` tag, and each project
  label belongs to exactly one track via the horizon's `track.projects`.
- Blocks from two tracks that overlap in time are **not** netted down. Ask once whether the
  overlap is real; if it is, both blocks count in full, and the day's track hours can exceed
  the wall-clock day. That is the honest record of doing two things at once.
- Empty when no horizon config resolves. The daily budget comparison is then not made rather
  than estimated.

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

One line per thing, each carrying a time span, what happened, and where the output landed.
Write what actually happened, not what the plan said. Three to six lines on a normal day.
A line that could describe any day is not worth writing.

## Not done → carry forward

{{not_done_carry_forward}}

Written for tomorrow's morning brief, which reads this section without the rest of the page.
Each item has to stand on its own a day later: name the thing, say why it did not happen,
and say what now depends on it. Usually one to three items; a list of eight means the plan
was wrong, and that is worth saying instead.

## Extra bonus

{{extra_bonus}}

Unplanned work that actually happened. If the user did not mention any, ask before writing the journal — never conclude there was none.

## Tomorrow's seeds ({{tomorrow_date}})

{{tomorrows_seeds}}

Three to five items, each specific enough to schedule without rereading anything else. This
is what tomorrow's plan gets built from, so vagueness here costs twice.

## Time-on-task

{{time_on_task}}

States the hours, which `focusHours.strategy` produced them, and any gap between logged time
and observed work. A number read off a worklog is not the same claim as one reconstructed
from commits — say which it is.

When two blocks from different tracks overlapped, say so and say that both were counted in
full, so the reader understands why the track hours exceed the wall clock.
