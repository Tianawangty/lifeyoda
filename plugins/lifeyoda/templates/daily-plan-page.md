# Daily Plan Page Template

Part of the public toolkit. Not user-specific configuration.

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

Block names follow the naming protocol: `{typeEmoji} [{project}] {verb}: {object}`. They must match the planning-calendar event titles exactly.

## ✅ Today's checklist

{{todays_checklist}}

Carry-over items are marked inline, for example `*(⤳ carried over)*`.

## 📌 Notes

{{notes}}

Notes carry: fixed constraints and travel buffers, blocked work that was deliberately not scheduled, deadlines being planned around, and which blocks were mirrored to the planning calendar.

## Fallback Body

When wrapup must create a Daily Plan row because none was made that day, the body contains only:

See journal
