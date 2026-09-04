# Demo Fixtures

Synthetic data for demo mode. Every value here is invented. Nothing was copied from a real
inbox, calendar, Notion database, or repository, and nothing here belongs to a real person.

Demo mode exists for two reasons. A new user can run all four commands before authorizing
a single connector, and see what the toolkit produces rather than reading about it. And a
change to a workflow can be compared against a fixed baseline, because these inputs never
move.

## Dates are relative

`manifest.json` is the authority and the first file to read. Connector fixtures store
offsets from the run date (`T+0`, `T-1`, `T+1`); `horizon.json` holds real dates because it
is validated against the real schema, and the manifest carries the anchor to shift it by.

So demo output is dated around today, whenever today is. Yesterday is deliberately a
*partial* day: one checklist item went unchecked and carries forward, which is what makes
the morning brief's carry-forward path visible.

`--demo-date YYYY-MM-DD` pins the day when two runs need to be compared.

## Files

| File | Stands in for |
| --- | --- |
| `manifest.json` | the date rules themselves — read first |
| `local.json` | the private config, with placeholder ids that resolve to nothing |
| `horizon.json` | the private horizon config |
| `calendar-events.json` | Google Calendar reads, including one already-written planning block |
| `notion-previous-day.json` | yesterday's Daily Plan row and Daily Journal |
| `mail-and-messages.json` | Gmail label reads and Slack DMs and mentions |
| `active-project.json` | `SESSION_REPORT.md`, project notes, and `git log` |

`local.json` and `horizon.json` are validated against the real schemas by
`scripts/check.py`, so a schema change that would break a user's config breaks the demo
first.

## What demo mode must not do

`/lifeyoda:apply-planner` in demo mode prints what it would write and stops. It must never
create a Notion page or a calendar event, whether or not a connector happens to be
available.

## Adding to these files

Invent the data. Not "realistic" data, not real data with the names changed, and never an
excerpt of a real source. Addresses use `example.com`, which is reserved for exactly this.
