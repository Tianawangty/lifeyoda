# LifeYoda

A workflow kit for a daily planning assistant, shared between Claude Code and Codex Desktop.

The loop:

1. **Plan.** Read a bounded set of high-signal sources — calendars, checklist pages, the active repo, yesterday's plan and journal. Produce a Morning Brief, ask one round of questions, produce a Draft Day Plan. Write nothing.
2. **Apply.** Only after confirmation, write one Daily Plan row to Notion and mirror its timed blocks to a single planning calendar.
3. **Wrap up.** Reconcile what actually happened, set the plan's status, and create the matching Daily Journal.

Notion is the source of truth. The calendar mirror is one-way and never read back.

## Running it (Claude Code)

The three commands live in `.claude/commands/`, so they are available when Claude Code is working in this directory:

```
/daily        Morning Brief + Draft Day Plan   (read-only)
/apply-plan   write the confirmed plan
/wrapup       reconcile and journal
```

Before the first run, copy `private.example/local.example.json` to `private/local.json` and fill in your own IDs. `config/local.schema.json` documents every field.

## Configuration

Public, committed:

- `config/public.defaults.json` — generic behaviour: naming protocol, emoji pool, page sections, source limits
- `config/local.schema.json` — the shape private config must satisfy

Private, never committed:

- resolved as `$LIFEYODA_CONFIG` → `~/.lifeyoda/local.json` → `private/local.json`
- `private/**` is gitignored

Private means: Notion page/block/database/data-source IDs, calendar IDs, Gmail labels, Slack IDs, checklist-source locators, repo names and local paths.

## Design notes

Three choices that are easy to get wrong:

- **The Daily Plan's date key is its title**, not its `Date` column. `Date` is a Notion `created_time` property, so a row backfilled a week later carries the wrong date on purpose — that mismatch is how you tell it was written after the fact.
- **Calendar dedupe re-reads the calendar** rather than storing sync state in Notion. Delete a block by hand and the next apply recreates it. This keeps the Notion schema minimal and avoids stale "already synced" flags.
- **Block names follow one protocol** across the Notion schedule table and the calendar: `{typeEmoji} [{project}] {verb}: {object}`. The `[project]` tag is the dedupe anchor.

## Runtime split

Both runtimes read the same `workflows/*.md`.

- **Claude Code** — manual trigger, direct calendar connectors.
- **Codex Desktop** — scheduled morning run; can fall back to Slack notifications as an Outlook Calendar proxy when a school account will not connect directly. Prompts live in `runtimes/codex-desktop/` and are not yet verified.

## Status

Working scaffold, not a packaged plugin. `LICENSE` has not been chosen, so this is not yet licensed for reuse. See `CLAUDE.md` for architecture details and the open next steps.
