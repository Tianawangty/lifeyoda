# The Horizon Layer

The daily layer can only see today. The horizon layer is what today inherits from.

It holds one terminal goal, the terms the horizon spans, the deadlines that cannot move, and the tracks whose milestones were derived by counting backwards from that goal. `/horizon` reads it and reports; `/daily` reads it and folds the near ones into the Morning Brief. Neither writes to it. Status changes are edits made by hand, which is deliberate: marking a milestone done should cost a moment of thought.

## Files

| File | Committed | Holds |
| --- | --- | --- |
| `config/horizon.schema.json` | yes | the authority on the file's shape |
| `config/public.defaults.json` | yes | `horizon.lookaheadDays`, `horizon.confidenceLevels` |
| `private.example/horizon.example.json` | yes | a complete structure with placeholder values |
| `private/horizon.json` | **no** | the real goal, deadlines, and milestones |

Resolution order is the same as every other private config: `$LIFEYODA_CONFIG`, then `~/.lifeyoda/horizon.json`, then `private/horizon.json`. First hit wins.

## Backward derivation

Forward planning asks what can be finished by December given what is happening now. It produces a list that is always plausible and never binding, because nothing on it is anchored to anything.

Backward derivation starts at the terminal goal and asks what has to be true the week before, and the week before that, until the chain reaches today. Every date it produces carries a reason: it is that date because of what follows it. That is what makes the chain load-bearing. When one link slips a week, everything downstream of it slips a week too, and the slip is visible immediately instead of at the end.

The mechanics are simple enough to state in three rules:

1. The terminal goal is a single fixed date. There is exactly one.
2. Hard deadlines are the dates between here and there that no amount of rescheduling can move. They are the skeleton.
3. Milestones hang off that skeleton by `dependsOn` edges. The longest chain of those edges to the next hard deadline is the critical path — the part where a one-day slip costs one day everywhere after it.

The `dependsOn` graph must stay acyclic. A cycle is not a scheduling problem to work around; it means two things have each been declared a prerequisite of the other, and one of those declarations is wrong.

## Three confidence levels

Not every date is knowable to the same degree, and flattening them into one list is how an assumption ends up being treated as a commitment.

**VERIFIED** — read from an authoritative published source, with the source recorded next to it. A published term schedule, a programme's filing deadline. If the source page changes, the date can be re-checked against the same place, which is why `source` is not decorative.

**DERIVED** — nobody publishes this date. It was computed backwards from constraints that are themselves verified. A launch date is the usual example: the organisation publishes the submission deadline that follows it, so the launch has to happen far enough before that deadline to leave room for corrections, and the number of weeks is a judgment call.

**INFERRED** — guessed from a pattern, such as last year's date for the same recurring event. Weakest of the three. Never presented as settled, and never used as the anchor for a chain.

### Why a DERIVED date must carry a companion milestone

A DERIVED date is a decision the people entitled to make it have not made yet. It sits in the file looking exactly like a VERIFIED date — same format, same field, same position in the chain — and after a few weeks of reading it in a brief every morning it starts to feel equally real. Then the date arrives, and the people who would have had to agree to it were never asked.

The rule that prevents this: **every DERIVED deadline carries a milestone whose only job is to get the date confirmed.** That milestone has its own target date, well before the derived date, and it sits on the critical path like anything else. The moment it completes, the deadline's confidence is upgraded to VERIFIED and its source rewritten to name whoever agreed. Until then, `/horizon` shows the confidence label every time it shows the date.

A DERIVED deadline with no companion milestone is a defect in the config, and `/horizon` reports it as one.

## The scheduled/completed split, again

The daily layer already draws one line hard: **a calendar records what was scheduled; whether it got done lives somewhere else.** The Daily Plan checklist and the Journal's carry-forward section hold completion; the planning calendar is only corroboration.

The horizon layer keeps the same line, one level up. Milestone `status` lives in the horizon file and in the tracker rows that mirror it. No calendar event, in the planning calendar or anywhere else, is ever read back to decide whether a milestone completed. A block on the calendar for a milestone means three hours were set aside for it, nothing more. This is why the horizon layer stores `notionPageId` but no calendar event id: the tracker row is the mirror, the calendar is not.

The practical payoff is that a week where every scheduled block happened and no milestone advanced looks exactly like what it is, instead of looking like progress.

## How the daily layer consumes it

`/daily` reads the horizon during its Source Sweep and pulls two things:

- milestones whose `targetDate` falls inside `lookaheadDays` — these go to **Later / FYI**
- milestones whose `targetDate` has already passed while `status` is not `done` — these go to **Key items**, because a slip nobody looks at compounds

The Draft Day Plan's Assumptions block then shows the week's per-track time budget derived from `weightPct` next to the effort actually recorded, which comes from the `Focus Hours` and `Projects Touched` that the wrapup workflow writes to the Journal. Budget on one side, recorded effort on the other. That comparison is the point of giving tracks weights at all: a track that keeps losing its hours to another one shows up as a number rather than a feeling.

## Weights

`weightPct` is a share of the working week, and the weights are expected to sum to 100. A track at `0` is dormant — it has milestones and dates but no hours of its own, and when it wakes up it borrows from a named track. `/horizon --week` states the borrowing explicitly rather than quietly rebalancing, because the borrowing is the decision worth seeing.

Weights budget the week; they do not schedule it. `/horizon --week` produces the shape, `/daily` turns one day of that shape into blocks.
