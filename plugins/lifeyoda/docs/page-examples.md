# Page Examples

Two filled-in pages, so the shape of a good one is visible rather than described. Both use
the demo fixtures — a small team shipping a widget app, with a `build` track and a
`research` track — so nothing here belongs to a real person or project.

Read these alongside `templates/daily-plan-page.md` and `templates/daily-journal-page.md`.
The templates say what each section is for; these show what filling it well looks like.

The point of an example is calibration, not imitation. Match the density and the level of
specificity, not the wording.

---

## Daily Plan — `Wed, September 3, 2026`

Row properties: `Status: Planned`, icon picked at random from `dailyPlan.emojiPool`,
`Focus` holding the three bullets below.

**Focus**

- Decide which of the two migration PRs lands first
- Draft the UX interview findings — carried from yesterday
- Push the A/B rollout to full allocation

### ⏰ Schedule

| Time | Block |
| --- | --- |
| 09:00–09:30 | 🔧 [widget-app] Decide: which migration PR lands first |
| 10:00–11:00 | 🗣 [widget-app] Meet: Standup — v2 pilot readout · on calendar |
| 13:00–15:00 | ✍️ [widget-research] Draft: UX interview findings |
| 17:00–18:00 | 🔬 [widget-app] Run: A/B rollout to full allocation |

Four blocks, not eight. The two travel buffers and the protected lunch are not rows here —
they are constraints, and they belong in Notes.

### ✅ Today's checklist

- 🔧 [widget-app] Decide: which migration PR lands first
- 🗣 [widget-app] Meet: Standup — v2 pilot readout · on calendar
- ✍️ [widget-research] Draft: UX interview findings *(⤳ carried over)*
- 🔬 [widget-app] Run: A/B rollout to full allocation

One line per scheduled block, in the same order and with the same names. A carry-over is
marked inline so tomorrow's brief can see it was not new work.

### 📌 Notes

- Standup is in Room 214, so 09:30–10:00 and 11:00–11:30 are travel buffers. Nothing is
  scheduled inside them.
- Lunch 12:00–13:00 is protected.
- Not scheduled, blocked upstream: the event-schema regression test. It waits on the
  renamed columns landing in staging.
- Milestone `build-2` was due 3 days ago and blocks `build-3`. The 17:00 block is the
  first move against it.
- Blocks mirrored to the planning calendar: three LifeYoda blocks. Standup already existed
  on Demo Work, so it stayed in the schedule but was not mirrored.

Notes carry what the schedule cannot: why a slot is unavailable, what was deliberately not
scheduled and why, which deadline the day is shaped around, and what reached the calendar.

---

## Daily Journal — `Tue, September 2, 2026`

Row properties: icon `📓` because the day was partial, `Date: 2026-09-02`,
`Focus Hours: 3.5`, `Track Hours: build 2; research 1.5`,
`Projects Touched: widget-app, widget-research`.

### What got done

- 09:00–11:00, 🔬 [widget-app] pilot rollout check ran clean. Both arms are live and the
  dashboard at `/pilot` is reporting.
- 10:30–12:00, ✍️ [widget-research] first pass at the UX interview findings. Structure only,
  no prose yet.
- Fixed a duplicate-id bug in the event schema that had been silently dropping 40 rows.

Each line carries a time span, what happened, and where the output is. Write what actually
happened, not what the plan said. Three to six lines on a normal day; a line that could
apply to any day is not worth writing.

### Not done → carry forward

- **UX interview findings — nothing drafted.** The rollout check took the whole morning.
  Milestone `research-1` wants them in 2 days.

Written for tomorrow morning, which reads this section without the rest of the page. Each
item has to stand on its own a day later: name the thing, say why it did not happen, and
say what now depends on it.

### Extra bonus

- The duplicate-id fix was not on the plan. It surfaced while reading rollout logs and was
  worth doing immediately, because every downstream count was wrong until it landed.

Unplanned work that actually happened. If the user mentioned none, ask before writing the
journal — never conclude there was none.

### Tomorrow's seeds (2026-09-03)

- Decide which of the two migration PRs lands first. Both touch the same migration, and a
  teammate is waiting on the answer.
- Draft the UX interview findings, properly this time. Give it the largest unbroken block.
- Push the A/B rollout to full allocation — `build-2` is already 3 days past due.

Three to five items, each specific enough to schedule without rereading anything. This is
the section tomorrow's plan is built from, so vagueness here costs twice.

### Time-on-task

**3.5 hours**, from the worklog calendar.

Two blocks overlapped between 10:30 and 11:00, across two different tracks. Confirmed real,
so both count in full: `build 2; research 1.5` sums to 3.5 against 3.0 hours of wall clock.
That gap is the record of doing two things at once, not an error.

States the hours, where the number came from, and any gap between logged time and observed
work. A number read off a worklog is not the same claim as one reconstructed from commits —
say which it is.
