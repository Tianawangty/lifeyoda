# Demo Mode

Demo mode lets all four commands run with no private config and no authorized connectors.
It exists so a new user can see what the toolkit produces before deciding whether to spend
twenty minutes configuring it, and so a change to a workflow can be compared against a
fixed baseline.

## When it engages

Two triggers, and no others:

- **Automatically**, when no private config resolves at any of the three tiers.
- **On request**, when the invocation carries `--demo`, even if a real config exists.

Demo mode never engages because a connector is unavailable. A user with a real config and
a broken Notion connection needs to be told the connection is broken, not handed invented
data that looks like their day.

## Say so, every time

The first line of the output declares it, before any content:

```
⚠ Demo mode — this is invented sample data, not your schedule.
  No config found at ~/.lifeyoda/local.json.
  Run /lifeyoda:setup to configure your own.
```

When `--demo` was requested explicitly and a real config exists, say that instead: the
real config is being ignored on purpose.

Never blend the two. A single run reads either fixtures or live sources, never a mix,
because a brief that is half invented is worse than one that is entirely invented.

## Where the data comes from

`fixtures/` replaces every source. `fixtures/local.json` and `fixtures/horizon.json` stand
in for the private config; the rest stand in for the connectors:

| Instead of | Read |
| --- | --- |
| Google and Outlook calendars | `fixtures/calendar-events.json` |
| the previous Daily Plan and Journal | `fixtures/notion-previous-day.json` |
| Gmail and Slack | `fixtures/mail-and-messages.json` |
| the active repository | `fixtures/active-project.json` |

**Today is the real run date.** `fixtures/manifest.json` is the authority on how the
fixtures become dates, and it is the first file to read.

Connector fixtures store offsets — `T+0 10:00` is today at ten, `T-1 18:40` was yesterday.
`horizon.json` is the exception: it is validated against the real schema, which requires
`YYYY-MM-DD`, so it holds absolute dates and the manifest carries a `horizonAnchor`. Shift
every date in it forward by (run date − anchor), which preserves the chain's spacing exactly.

A fixed demo date was the earlier design, and it was wrong in a way that only shows up
later: a demo dated to a day months in the past reads as an abandoned project. Relative
dates are always plausible and never need maintaining.

`--demo-date YYYY-MM-DD` holds the day still. Comparing two runs of a changed workflow
needs that; without it the diff is all date noise.

## Writes

**Demo mode writes nothing.** Not to Notion, not to a calendar, not to disk, and not to
the fixtures themselves.

`/lifeyoda:apply-planner` is the command where this matters. In demo mode it prints the
Daily Plan row it would create and the calendar blocks it would mirror, then stops. It
must not create a page or an event even when a connector happens to be available and even
when the user confirms — the confirmation applies to invented data, so acting on it would
write invented data into a real workspace.

## Everything else is unchanged

Demo mode substitutes the inputs. It does not simplify the workflow: the same question
round, the same ranking, the same naming protocol, the same output sections. A demo run
that skipped the question round would demonstrate something the real toolkit does not do.
