# LifeYoda

A workflow kit for a daily planning assistant, packaged for both Claude Code and Codex/ChatGPT Codex.

The loop:

1. **Plan.** Read a bounded set of high-signal sources — calendars, checklist pages, the active repo, yesterday's plan and journal. Produce a Morning Brief, ask one round of questions, produce a Draft Day Plan. Write nothing.
2. **Apply.** Only after confirmation, write one Daily Plan row to Notion and mirror its timed blocks to a single planning calendar.
3. **Wrap up.** Reconcile what actually happened, set the plan's status, and create the matching Daily Journal.

Notion is the source of truth. The calendar mirror is one-way and never read back.

## Running it from this source checkout

The three commands live in `.claude/commands/`, so they are available when Claude Code is working in this directory:

```
/daily        Morning Brief + Draft Day Plan   (read-only)
/apply-planner   write the confirmed plan
/wrapup       reconcile and journal
/horizon      long-horizon planning view       (read-only)
```

These commands are local development conveniences. The installable Claude Code plugin exposes namespaced commands instead:

```
/lifeyoda:daily
/lifeyoda:apply-planner
/lifeyoda:wrapup
/lifeyoda:horizon
```

## Installing From Private GitHub

This repository now contains both marketplace surfaces:

- Claude Code marketplace: `.claude-plugin/marketplace.json`
- Codex marketplace: `.agents/plugins/marketplace.json`
- Shared plugin root: `plugins/lifeyoda/`

Claude Code:

```text
/plugin marketplace add Tianawangty/LifeYoda
/plugin install lifeyoda@lifeyoda
```

For development branch testing:

```text
/plugin marketplace add Tianawangty/LifeYoda@dev
```

Codex CLI:

```bash
codex plugin marketplace add Tianawangty/LifeYoda --ref dev
codex plugin add lifeyoda@lifeyoda
```

For ChatGPT/Codex workspace import, use source `https://github.com/Tianawangty/LifeYoda.git`, leave path empty, and use branch `dev` for testing or `main` for the stable package.

Before the first run, copy `private.example/*.json` to `~/.lifeyoda/` and fill in your own IDs. Do not edit the installed plugin cache. `config/local.schema.json` documents every field.

## Configuration

Public, committed:

- `config/public.defaults.json` — generic behaviour: naming protocol, emoji pool, page sections, source limits
- `config/local.schema.json` — the shape private config must satisfy

Private, never committed. Three locations resolve, first hit wins, and all three are equally supported — pick the one that matches how you run the toolkit:

| Location | Pick it when |
| --- | --- |
| `$LIFEYODA_CONFIG` | you switch between profiles, or keep config somewhere unusual |
| `~/.lifeyoda/` | you installed the plugin — this resolves from any working directory |
| `private/` in a source checkout | you are trying the toolkit out and have not chosen a home yet |

`~/.lifeyoda/` may be a real directory or a symlink to a folder you already back up. A symlink into a synced folder outside any git repository is worth considering: the files stay backed up, and no git command can reach them.

The source-checkout location has two properties worth knowing before you rely on it. It resolves only when the working directory is the checkout, so an installed plugin invoked from another project will not find it. And it is gitignored and untracked, so `git clean -xdf` deletes it and a fresh clone starts empty.

`private/**` is gitignored either way.

Private means: Notion page/block/database/data-source IDs, calendar IDs, Gmail labels, Slack IDs, checklist-source locators, repo names and local paths.

A repo `localPath` may be a single `$VAR` reference instead of a literal path, expanded from the environment at run time. Use it when a path embeds something you would rather keep out of a file — a cloud-storage folder named after your account email, for example. Define those variables in `~/.zshenv` rather than `~/.zshrc`: agent runtimes start non-interactive shells, which never source `.zshrc`. An unset variable, a path that does not exist, and a path that is not a git repository are all reported as unavailable; none of them is ever treated as a literal directory.

## Design notes

Three choices that are easy to get wrong:

- **The Daily Plan's date key is its title**, not its `Date` column. `Date` is a Notion `created_time` property, so a row backfilled a week later carries the wrong date on purpose — that mismatch is how you tell it was written after the fact.
- **Calendar dedupe re-reads the calendar** rather than storing sync state in Notion. Delete a block by hand and the next apply recreates it. This keeps the Notion schema minimal and avoids stale "already synced" flags.
- **Block names follow one protocol** across the Notion schedule table and the calendar: `{typeEmoji} [{project}] {verb}: {object}`. The `[project]` tag is the dedupe anchor.

## Runtime split

Both runtimes read the same packaged `workflows/*.md`.

- **Claude Code** — manual trigger through source commands or installed `/lifeyoda:*` commands.
- **Codex / ChatGPT Codex** — installed skills for the same flows; external connectors are optional and unavailable sources are reported rather than guessed.
- **Codex Desktop** — prompt materials remain in `runtimes/codex-desktop/`; scheduled tasks are created separately in Codex Desktop.

## Status

Private dual-runtime plugin package. `LICENSE` has not been chosen, so this is not licensed for public reuse. See `CLAUDE.md` for architecture details and the open next steps.
