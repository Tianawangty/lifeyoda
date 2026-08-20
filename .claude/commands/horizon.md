---
description: Long-horizon view. Counts back from the terminal goal through hard deadlines and track milestones. Reads config only, writes nothing.
argument-hint: "[nothing | --track <id> | --week]"
---

# /horizon

Show where the long horizon stands. **This command writes nothing** — not to Notion, not to any calendar, not to the horizon file itself. Status changes are made by editing the private horizon config by hand.

1. Read `config/public.defaults.json` for toolkit defaults, including `horizon.lookaheadDays` and `horizon.confidenceLevels`.
2. Resolve private horizon config in this order, first hit wins:
   - `$LIFEYODA_CONFIG`
   - `~/.lifeyoda/horizon.json`
   - `private/horizon.json`
3. If no private config resolves, say so and stop. Point at `private.example/horizon.example.json` as the template to copy. Do not invent a goal, a deadline, or a milestone.
4. `config/horizon.schema.json` is the authority on the file's shape. A key the schema does not know is a hard error, not something to ignore quietly.

Today is the current date in the daily config's timezone unless `$ARGUMENTS` names a date.

## Rules that hold in every mode

- A `DERIVED` date is not settled. Show the label with its confidence, and name the companion milestone that confirms it. If a `DERIVED` deadline has no companion milestone, that absence is itself a finding worth reporting.
- An `INFERRED` date is weaker still. Never present one as agreed.
- A milestone whose `targetDate` has passed while `status` is anything other than `done` is a **slip**, whether or not its status field says `slipped`. The dates decide, not the label.
- `dependsOn` edges must stay acyclic. If they do not, report the cycle and stop rather than printing a critical path that cannot exist.
- Completion status lives in the horizon file and the tracker, never on a calendar. A calendar records only what was scheduled.

## Mode: no argument — backward view

Report, in this order:

1. **Countdown** — weeks remaining to `terminalGoal`, and which term today falls in.
2. **Next hard deadline** — the nearest entry in `hardDeadlines` on or after today, with its confidence and source.
3. **Critical path** — the longest chain of `dependsOn` edges that has to complete before the next hard deadline, one line per link, with target dates. This is the part where slipping one link moves everything after it.
4. **Slipping now** — every milestone whose `targetDate` is in the past and whose `status` is not `done`, oldest first, with how many days late and what it blocks downstream.

If nothing is slipping, say so in one line rather than printing an empty heading.

## Mode: `--track <id>` — one track expanded

Expand the single track whose `id` matches. Show its `label`, its `weightPct`, and every milestone in target-date order with status, dependencies, and `evidence`. Mark which milestones sit on the critical path and which have slack.

If the id matches no track, list the available ids and stop.

## Mode: `--week` — this week's advance

1. Select the milestones to advance: anything due inside `lookaheadDays`, anything already slipping, and anything on the critical path to the next hard deadline.
2. Derive a time budget from `weightPct`. Ask for the number of working hours available this week if it is not already known, then split those hours across tracks in proportion to their weights. A track at `weightPct: 0` gets no hours of its own and must borrow from a named track, which the output states explicitly.
3. For each track, show budgeted hours next to the specific milestones the hours should go to.
4. Name the collisions. When two tracks want the same days, say which one yields and why — an external hard deadline outranks an internal target date.

Weights are a budget, not a schedule. `/horizon --week` produces the shape of the week; `/daily` turns a day of it into blocks.

## Output discipline

Plain prose and short tables. No connector checks, no tool names, no process commentary. Every date rendered `YYYY-MM-DD` so it can be compared against the config without arithmetic.
