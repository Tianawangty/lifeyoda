# CLAUDE.md

This file provides guidance to Claude Code and Codex when working with this repository.

## What this repo is

LifeYoda is a prose-only workflow kit for a daily planning assistant. There is no build, no test suite, and no executable code — the "programs" are markdown workflows that an agent reads and follows, plus JSON config that parameterizes them.

Two runtime families share the same workflows:

- **Claude Code** — manual, via slash commands in `.claude/commands/`. Reads calendars directly.
- **Codex / ChatGPT Codex** — via packaged skills in `plugins/lifeyoda/skills/`. Codex Desktop prompt materials live in `runtimes/codex-desktop/`; a scheduled task is created separately.

The installable plugin package lives in `plugins/lifeyoda/`. It is self-contained so Claude Code and Codex can copy it into their plugin caches without relying on files outside the plugin root.

## Commands

Run from this repo directory (project-level Claude Code slash commands):

| Command | Reads | Writes |
| --- | --- | --- |
| `/daily` | `workflows/morning-brief-and-plan.md` | nothing |
| `/apply-planner` | `workflows/apply-daily-plan.md` | one Notion Daily Plan row + planning-calendar blocks |
| `/wrapup` | `workflows/wrapup-journal.md` | Daily Plan status + one Daily Journal |
| `/horizon` | horizon config, resolved like every private config | nothing |

Installed Claude Code commands are namespaced:

```
/lifeyoda:daily
/lifeyoda:apply-planner
/lifeyoda:wrapup
/lifeyoda:horizon
```

Codex installs the same behavior as skills: `lifeyoda-daily`, `lifeyoda-apply-planner`, `lifeyoda-wrapup`, and `lifeyoda-horizon`.

The sequence is always `/daily` → user confirms → `/apply-planner`, and `/wrapup` at end of day. `/daily` never writes; `/apply-planner` never runs without a confirmed draft in the same conversation.

Verify config health with:

```bash
# 1. every repo path the config names actually resolves
zsh -c 'for v in PROJECT_A_ROOT LIFEYODA_ROOT PROJECT_B_ROOT PROJECT_C_ROOT; do
  p="${(P)v}"
  if [ -z "$p" ]; then printf "  %-15s UNSET\n" "$v"
  elif git -C "$p" rev-parse --is-inside-work-tree >/dev/null 2>&1; then printf "  %-15s OK\n" "$v"
  elif [ -d "$p" ]; then printf "  %-15s NOT-A-REPO   %s\n" "$v" "$p"
  else printf "  %-15s MISSING      %s\n" "$v" "$p"; fi
done'

# 2. the config parses and stores no literal paths
python3 -c "import json,os;d=json.load(open(os.path.expanduser('~/.lifeyoda/local.json')));s=d['sources'];print([m['localPath'] for m in s['projectMapping']], s['activeProject']['primary']['localPath'])"

# 3. nothing private is staged for a commit
git grep --cached -nIiE "@group\.calendar\.google\.com|@gmail\.com|/Users/" \
  | grep -vE "^(CLAUDE|AGENTS)\.md:|^docs/public-release-checklist\.md:"   # these carry the patterns themselves
git ls-files private/                                                          # expect only .gitkeep
git add -An . | grep -c "private/"                                             # expect 0
```

Run check 1 whenever a repo moves, a machine changes, or `/daily` reports anything other than `4/4`. It is the same check the workflow's Config Health step performs; running it by hand is how you tell a real failure from a workflow that skipped the step.

## Config resolution

Every workflow resolves private config in this order, first hit wins:

1. `$LIFEYODA_CONFIG`
2. `~/.lifeyoda/local.json`
3. `private/local.json` when running from a source checkout

`config/public.defaults.json` is committed and holds the toolkit's generic behaviour — naming protocol, emoji pool, section names, source limits. `config/local.schema.json` is the authority on the private config's shape (`additionalProperties: false` at the top level, so a typo'd key is a hard error, not a silent ignore).

`private/**` is gitignored. **Real Notion IDs, calendar IDs, and repo paths live only in the private layer, never in a workflow, a doc, or this file.** `private.example/` mirrors the structure with placeholders.

Where that layer lives is the user's choice, and all three tiers are supported equally:

| Where | Good for |
| --- | --- |
| `$LIFEYODA_CONFIG` | a path you want to switch between profiles |
| `~/.lifeyoda/` — a real directory, or a symlink to a synced folder | installed plugins, since it resolves from any working directory |
| `private/` in a source checkout | trying the toolkit out before committing to a location |

The third tier only resolves when the working directory is the checkout, so an installed plugin invoked from elsewhere will not find it. It is also gitignored and untracked, which means `git clean -xdf` deletes it and a fresh clone starts with nothing — keep a copy elsewhere if you use it. Never edit the plugin cache.

This repo's owner uses tier 2 as a symlink into a cloud-synced folder that sits outside any git repository, which keeps the files backed up while putting them out of reach of every git operation.

A repo `localPath` may be written as a single `$VAR` instead of a literal path. That form exists so a path embedding personal data — an account email inside a cloud-storage folder name, for example — never enters a config file. Set those variables in `~/.zshenv`, not `~/.zshrc`: Claude Code's Bash tool runs a **non-interactive login zsh**, which reads `.zshenv` and `.zprofile` and never sources `.zshrc`. Codex ships its own zsh and reads `.zshenv` on every invocation.

One known rough edge: `$LIFEYODA_CONFIG` is consulted as the first tier for `horizon.json` too, but its name describes a path to `local.json`. Setting it would point the horizon lookup at the wrong file. It is unset here, so nothing triggers today.

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
- Marketplace surfaces:
  - Claude Code: `.claude-plugin/marketplace.json`
  - Codex: `.agents/plugins/marketplace.json`
  - plugin root: `plugins/lifeyoda/`
- **Claude Code installs are keyed on the plugin version.** The cache directory is named after it (`~/.claude/plugins/cache/lifeyoda/lifeyoda/<version>/`), and an install at a version already present is skipped without a word — `/plugin marketplace update` refreshes the marketplace metadata only, not the installed plugin. So any change to `plugins/lifeyoda/` needs the version bumped in all four places (`plugins/lifeyoda/.claude-plugin/plugin.json`, `plugins/lifeyoda/.codex-plugin/plugin.json`, and two lines in `.claude-plugin/marketplace.json`) or Claude Code keeps running the old text. Codex does not have this problem: `.agents/plugins/marketplace.json` pins no version and `codex plugin add` re-copies unconditionally.
- `runtimes/claude-code/` is now a legacy prompt scaffold. `.claude/commands/*.md` remains the source-checkout command surface; `plugins/lifeyoda/commands/*.md` is the installable Claude plugin surface.
- A `PreToolUse:Write` hook in the user's Claude Code settings blocks new `.md` files outside an allowlist; this repo path is whitelisted. Local specifics are in `private/NOTES.md`.
- `LICENSE` still says no license is chosen, while both `plugin.json` files declare `"license": "Proprietary"`. The two disagree and either one blocks public reuse. See `docs/public-release-checklist.md`.
- The private layer lives outside this checkout. `private/` holds only `.gitkeep`; a `git clean -xdf` here destroys nothing.

## Next steps

Owner-specific context for all of these — which institution, which tracker, which repos — lives in `private/NOTES.md`.

**Long-horizon layer** — built. `/horizon` counts back from a terminal goal through hard deadlines and per-track milestones; `config/horizon.schema.json` fixes the shape, `docs/horizon-layer.md` explains the model, and `/daily` folds past-due milestones into Key items and upcoming ones into Later / FYI. Two questions the layer was going to settle are still open:

- whether the owner's project tracker becomes writable again, and whether a `Scheduled Date` property is reintroduced for cross-day scheduling — both were deliberately deferred to this layer
- whether the per-track budget in the Draft Day Plan's Assumptions block holds up against recorded effort once several weeks of Journals exist to compare against

**Repos not yet wired** — two candidate repos are listed in `private/NOTES.md`, and neither exists on disk as of 2026-08-31. Confirm whether they were abandoned before adding entries to `sources.activeProject.secondary` and `sources.projectMapping`. One stale course mapping was dropped; the corresponding Notion multi-select option was left alone so historical journal rows stay intact.

**`activeProject.secondary` is empty** — only the primary repo is mined for next steps. The personal-site repo was demoted to `projectMapping` alone, and a secondary repo is deliberately never opened by `/daily`: those signals reach the brief through a deadline calendar and the horizon track instead. Adding a repo to `secondary` means `/daily` will read its `SESSION_REPORT.md` and unfinished notes, so decide the privacy question before adding one.

**Packaging** — the dual-runtime package under `plugins/lifeyoda/` is now tracked in git, so the two plugin caches can be reinstalled from a commit. Remaining pre-release work — license choice, the two publication routes, the `.app.json` connector IDs, install verification from `main`, and synthetic dry-run fixtures — is inventoried with measured exposure figures in `docs/public-release-checklist.md`.

**`state.json` is read but never written** — `workflows/morning-brief-and-plan.md` lists it as an input and `config/README.md` calls it "run state written by the workflows", but no workflow contains a write step. It has held its initial nulls since the day it was created, so `lastSuccessfulMorningRunAt` proves nothing about whether a run happened. Either add the write step or drop the file: a state file that is always empty is worse than no state file, because it invites exactly the wrong inference.

**Codex Desktop** — prompt materials exist and are packaged, but the actual scheduled task is still created separately in Codex Desktop.
