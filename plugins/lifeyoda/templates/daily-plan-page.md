# Daily Plan Page Template

Part of the public toolkit. Not user-specific configuration.

`docs/page-examples.md` shows this page filled in. Match its density and specificity, not
its wording.

## Row Properties

`Daily` (title):
- Format `{weekday_short}, {month_full} {day}, {year}` — for example `Wed, June 17, 2026`.
- **This title is the date key.** Look up and dedupe rows by it.

Icon:
- One emoji picked at random from `dailyPlan.emojiPool` when the row is created.
- Never `✅` or `📓` — those belong to the journal.

`Date` (created_time):
- Read-only, set automatically by Notion. Never written by this toolkit.
- Disagreement between `Date` and the title means the row was backfilled. That is a signal, not an error.

`Focus` (text):
- 3-5 bullet points summarizing the day.

`Status` (select):
- `Planned` when created by apply-daily-plan.
- `Done` or `Partial` when updated by wrapup-journal.

`📝 Daily Journal` (relation):
- Set by wrapup-journal when the matching journal is created.

## Page Body

## ⏰ Schedule

| Time | Block |
| --- | --- |
{{schedule_rows}}

One row per block of work or source-calendar commitment, in time order. Mirrored block
names follow the naming protocol `{typeEmoji} [{project}] {verb}: {object}`, and must
match the planning-calendar event titles exactly. Source-calendar commitments that were
already on a calendar are kept in the table for a complete timeline, but the source-only
marker and provenance from the draft are not written here.

Typically three to six rows. Travel buffers, protected blocks, and lunch are **not** rows —
they are constraints, and they belong in Notes. A day with ten rows is a task list that has
been pasted into a schedule.

## ✅ Today's checklist

{{todays_checklist}}

One line per scheduled block, in the same order and carrying the same name, so the two
sections can be compared at a glance. Carry-over items are marked inline, for example
`*(⤳ carried over)*` — tomorrow's brief uses that marker to tell a repeat from new work.

## 📌 Notes

{{notes}}

Notes carry what the schedule cannot: fixed constraints and travel buffers, work that was
deliberately not scheduled and why, the deadline or milestone the day is shaped around, and
which blocks reached the planning calendar.

Three to six bullets. Each one answers a question the schedule raises — why that slot is
empty, why an obvious task is missing — rather than restating what is already in the table.

## Fallback Body

When wrapup must create a Daily Plan row because none was made that day, the body contains only:

See journal
