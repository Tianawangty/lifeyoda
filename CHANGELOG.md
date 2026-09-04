# Changelog

Versions follow [semantic versioning](https://semver.org/). A change to
`config/local.schema.json` that removes a field or an enum value is breaking.

## 1.0.0 — 2026-09-03

First public release.

### Commands

- `/lifeyoda:daily` — morning brief and a draft day plan. Writes nothing.
- `/lifeyoda:apply-planner` — writes the confirmed plan to Notion and the planning calendar.
- `/lifeyoda:wrapup` — reconciles the day and creates the matching journal.
- `/lifeyoda:horizon` — the long view, with the critical path and any defects in the chain.
- `/lifeyoda:setup` — creates or adopts the two Notion databases, picks calendars and
  sources, and works backwards from a long-term goal to build a milestone chain. Re-run it
  to change any one part.
- `/lifeyoda:doctor` — read-only health check across config, database shape, calendar
  access, repository paths, and enabled sources.

### Sources

- Google Calendar and Outlook Calendar, both with named calendars and roles.
- Gmail and Slack, off by default and scoped to the labels and message kinds you name.
- Local git repositories, and an optional long-horizon config.

### Calendar hygiene

A block that is already an event on one of your own calendars is not copied to the plan
calendar. It still appears in the Notion schedule, marked `· on calendar`, so the day reads
as a whole. Plan events are created with no attendees, so the calendar provider does not
mirror them onto a second calendar, and each carries one reminder 15 minutes before.

### Demo mode

All four planning commands run on invented fixtures with no config and no connectors, and
say so on the first line. Dates are relative to the run date, so the sample never goes
stale. `--demo` forces it; `--demo-date` pins the day so two runs can be compared.

### Privacy levels

Each destination carries an optional `sharing` level — `private`, `shared`, or unset. On a
`shared` or unset calendar the event title is cut at the colon and the description is left
empty, so a calendar someone else can read never carries the specifics. Unset behaves as
`shared`. The `[project]` tag survives at every level, and absolute paths, credentials,
dataset or account identifiers, and email addresses never reach a calendar at all.

### Effort tracking

A horizon track declares the project labels that roll up into it. The Daily Journal records
`Track Hours`, derived from the `[project]` tag on each worklog calendar block. Blocks from
two tracks that overlap are confirmed once and then both counted in full, so a day's track
hours can exceed its clock hours.

### Known limitations

- No known limitations.
