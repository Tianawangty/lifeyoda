# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

LifeYoda is a prose-only workflow kit for a daily planning assistant. There is no build, no test suite, and no executable code — the "programs" are markdown workflows that an agent reads and follows, plus JSON config that parameterizes them.

Two runtimes share the same workflows:

- **Claude Code** — manual, via slash commands in `.claude/commands/`. Reads calendars directly.
- **Codex Desktop** — scheduled at 07:30, prompts in `runtimes/codex-desktop/`. Uses Slack as an Outlook proxy because a school Outlook account can fail to connect directly behind extra security prompts. Not verified yet.

## Commands

Run from this repo directory (they are project-level slash commands).

| Command | Reads | Writes |
| --- | --- | --- |
| `/daily` | `workflows/morning-brief-and-plan.md` | nothing |
| `/apply-planner` | `workflows/apply-daily-plan.md` | one Notion Daily Plan row + planning-calendar blocks |
| `/wrapup` | `workflows/wrapup-journal.md` | Daily Plan status + one Daily Journal |
| `/horizon` | horizon config, resolved like every private config | nothing |

The sequence is always `/daily` → user confirms → `/apply-planner`, and `/wrapup` at end of day. `/daily` never writes; `/apply-planner` never runs without a confirmed draft in the same conversation.

Verify config health with:

```bash
python3 -c "import json;d=json.load(open('private/local.json'));print(sorted(d))"
git check-ignore -v private/local.json    # must print a match
```

## Config resolution

Every workflow resolves private config in this order, first hit wins:

1. `$LIFEYODA_CONFIG`
2. `~/.lifeyoda/local.json`
3. `private/local.json`

`config/public.defaults.json` is committed and holds the toolkit's generic behaviour — naming protocol, emoji pool, section names, source limits. `config/local.schema.json` is the authority on the private config's shape (`additionalProperties: false` at the top level, so a typo'd key is a hard error, not a silent ignore).

`private/**` is gitignored. **Real Notion IDs, calendar IDs, and local repo paths live only there.** Never inline them into a workflow, a doc, or this file. `private.example/` mirrors the structure with placeholders.

## Architecture

The three workflows form a loop with Notion as the source of truth and a single write-only planning calendar:

```
/daily     read calendars, checklist sources, active repo,
           previous Daily Plan + Journal
             → Morning Brief
             → ONE round of questions
             → Draft Day Plan            (nothing written)

/apply-planner  Notion Daily Plan row  +  planning calendar blocks

/wrapup    Daily Plan Status → Done/Partial
           Daily Journal (icon ✅/📓, linked both ways)
```

Four facts that are not obvious from any single file:

**1. The Daily Plan's date key is the title, not the `Date` column.** `Date` is a `created_time` property — read-only, automatically stamped when the page is created. Look rows up by title (`Wed, June 17, 2026`). A `Date` that disagrees with the title means the row was backfilled after the fact. That is a deliberate signal. Never try to correct it.

**2. Completion status is not on the calendar.** A calendar records what was *scheduled*. Whether it got *done* lives in the Daily Plan's `✅ Today's checklist` checkboxes and the Journal's `Not done → carry forward` section. The morning brief reads those two; the calendar is only corroboration (four blocks scheduled but three items checked is a gap worth naming).

**3. Calendar dedupe reads the destination.** Before writing, `/apply-planner` lists the planning calendar for that date and compares on start time plus the `[project]` tag. No sync state is stored in Notion — no event id, no synced checkbox. This is why the naming protocol matters: the `[project]` tag is the dedupe anchor. The predecessor tool stored ids on tracker rows instead, which covered only tasks that happened to be tracker rows and went stale whenever an event was deleted by hand.

**4. Outlook returns real UTC, and every source is normalized once, at capture.** `outlook_calendar_search` returns `{dateTime, timeZone}` pairs where the string is wall-clock *in the zone it names*. When that zone is `UTC` the time really is UTC and must be converted: `19:00 UTC` is `15:00 EDT`. Google Calendar is the opposite case — its times already carry an offset, so converting them again lands them four hours early. Convert each source by its own rule at the moment it is read, so no list ever holds converted and raw times side by side. Earlier revisions of this file claimed Outlook returned already-local strings and set `returnsWallClockAsUtc: true`; that was wrong, and the worked example offered as proof (`12:35` returned, `08:35 AM` in the body) was always evidence for plain UTC. Corrected 2026-08-27 after two consecutive days of body-text verification. Always render with the zone abbreviation shown.

## Naming protocol

Schedule-table rows and calendar events use one format, defined in `naming.template`:

```
{typeEmoji} [{project}] {verb}: {object}
```

`typeEmoji` comes from `naming.typeEmoji`. `[project]` is the dedupe anchor and must stay stable even if someone edits the description by hand. Titles must survive phone truncation — emoji and project tag readable in the first ~25 characters.

## Read-only boundaries

- The planning calendar is the **only** writable calendar. Every other calendar is read-only, and calendar events are never read back into Notion.
- Everything under `destinations.privateReadOnly` is a signal source that must never be written.
- Task trackers, course databases, and My Tasks-style scratch lists are out of scope entirely. Ad hoc errands are collected by asking during `/daily`, not from a database.

## Repo state notes

- Private repository. Two branches: `main` (stable) and `dev` (working). Work branches off `dev`.
- `runtimes/claude-code/` is a stale scaffold from before the commands were built: `plugin.json` sits at the wrong path and its `commands/*.prompt` files are not loadable. Left in place as the seed for future packaging. `.claude/commands/*.md` is what actually runs.
- A `PreToolUse:Write` hook in the user's Claude Code settings blocks new `.md` files outside an allowlist; this repo path is whitelisted. Local specifics are in `private/NOTES.md`.
- `LICENSE` still says no license is chosen. That blocks public release.

## Next steps

Owner-specific context for all of these — which institution, which tracker, which repos — lives in `private/NOTES.md`.

**Long-horizon layer** — built. `/horizon` counts back from a terminal goal through hard deadlines and per-track milestones; `config/horizon.schema.json` fixes the shape, `docs/horizon-layer.md` explains the model, and `/daily` folds past-due milestones into Key items and upcoming ones into Later / FYI. Two questions the layer was going to settle are still open:

- whether the owner's project tracker becomes writable again, and whether a `Scheduled Date` property is reintroduced for cross-day scheduling — both were deliberately deferred to this layer
- whether the per-track budget in the Draft Day Plan's Assumptions block holds up against recorded effort once several weeks of Journals exist to compare against

**Repos not yet wired** — additional project repos are listed in `private/NOTES.md`. Each needs an entry in `sources.activeProject.secondary` and `sources.projectMapping`. One stale course mapping was dropped; the corresponding Notion multi-select option was left alone so historical journal rows stay intact.

**Packaging** — deferred by explicit request. When it happens: move `.claude/commands/` to `commands/`, add `.claude-plugin/plugin.json` and `marketplace.json`, and move private config out of the repo to `~/.lifeyoda/` (a marketplace-installed plugin's directory is overwritten on update).

**Codex Desktop** — prompts exist but are unverified, and three of them hardcode this repo's absolute path.
