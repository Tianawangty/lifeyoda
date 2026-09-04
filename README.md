# LifeYoda

**A multi-track daily planner that runs inside Claude Code and Codex.**

> Life is not linear. Your planner shouldn't be either.

[![checks](https://github.com/Tianawangty/lifeyoda/actions/workflows/ci.yml/badge.svg)](https://github.com/Tianawangty/lifeyoda/actions/workflows/ci.yml)
[![license MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-d97757)
![Codex](https://img.shields.io/badge/Codex-plugin-10a37f)

<sub>Independent open-source project. Not affiliated with, endorsed by, sponsored by, or maintained by Anthropic or OpenAI. Claude Code and Codex are named only to describe the runtimes this toolkit runs inside.</sub>

✨ **Good things have a habit of happening at the same time. Your planner should be able to keep up.** ✨

LifeYoda is an agent-native planning kit for days that refuse to stay on one track. It
remembers where you’re headed, keeps the day you planned and the day you actually lived
side by side, and carries forward what still matters.

It is not another planner app with a shiny dashboard and a new place to forget to check.
Claude Code or Codex reads the Markdown workflows, uses the connectors you authorize, and
keeps the durable record in Notion, the calendar you choose for plan blocks, and a small
local config.

EVEN BETTER 🤪 **No streaks to protect and no productivity guilt. You close the day seeing everything you moved forward, not staring at everything you didn’t finish.**

```
/lifeyoda:daily           read calendars, mail, checklists, the active repo,
                          yesterday's plan and journal
                            → Morning Brief
                            → one round of questions in case missing anything
                            → Draft Day Plan for review

  [ you confirm or add anything at all — flexible daily input ]

/lifeyoda:apply-planner   one Notion Daily Plan row
                          + confirmed blocks on your chosen calendar

/lifeyoda:wrapup          reconcile what happened, set the plan's status,
                          create the matching Daily Journal

/lifeyoda:horizon         count back from a terminal goal through hard deadlines
                          and track milestones 
```

## 🧭 Does it hold up?

> **Used every day for months.**

Morning briefs, confirmed plans, and end-of-day journals, every day. It was built around
an actual routine, not a hypothetical productivity system. That is where the fussy little
rules came from: demo data says it is demo data, broken sources say they are broken, and a
calendar block never gets to pretend the work is done.

> **Life is not linear. Your planner should not pretend it is.**

You might be building a career, learning something new, running a side project, and somehow still having a life, all at the same time. That’s not unusual when you’re going places. Sometimes life simply has more than one good thing in motion. That is the shape this tool was built for: a busy life moving in several directions at once.

> **Five things it does differently from a general-purpose daily planner.**

- **It remembers the milestones you forget, and works backward from the ones you can’t afford to.**
  Name a goal a year out and `/lifeyoda:setup` walks backwards with you, one question at a
  time — what has to be finished before that, and how long does that take — until the steps
  are about two weeks apart. A date you computed rather than read somewhere gets marked as
  computed, and gets a companion milestone whose only job is to get it confirmed by whoever
  actually decides it. From then on the chain shows up in the morning brief on its own:
  what slipped, what it blocks, what is due next. Long-term goals stop living in the vague
  land of “eventually” and start having a say in what you do today.

- **It lets several tracks be real at the same time.**
  Real work does not always fit neatly into one task per time slot. Two projects can
  overlap, and the tool keeps both instead of forcing one to disappear. At wrapup, it
  splits effort across tracks, so attributed hours can exceed clock hours on purpose. The
  point is not perfect timekeeping. It is seeing where your energy actually went.

- **It refuses to confuse scheduled with done.**
  A calendar block means time was set aside. That is useful, but it is not completion. What
  you intended to do stays in the plan. What actually happened goes into the journal. If
  something slid for three days, it shows up as having slid for three days. No shame spiral,
  no quiet rewrite, no productivity theater with better lighting.

- **It reads signals, not everything with a timestamp.**
  A useful morning brief is small enough to finish. LifeYoda looks for the few things that
  can change today's plan: a direct ask, a hard deadline, a moved meeting, a slipped
  milestone, a repo change that blocks the next step. Mail and Slack are signal sources,
  not extra task lists in disguise.

- **Nothing heavy to install or maintain.**
  Markdown and JSON, read by Claude Code or Codex through connectors you authorize. Notion's
  free tier is enough. No database, no server, no build step, and no local footprint that
  grows as you use it.


## 🧰 Prerequisites

You can run demo mode before authorizing anything. For your real schedule:

- **Claude Code** or **Codex** — the toolkit is a plugin for either. [See how to install it](#install).
- **Notion** — required for Daily Plan and Daily Journal storage. `/lifeyoda:setup` can create the two databases it needs, with the right properties already in place.
- **A calendar** — Google or Outlook. At least one calendar has to be writable, because confirmed plans become calendar blocks.
- **Gmail, Slack** — optional MCP connection, default at off until you turn them on.

**Your planner shouldn’t become another project to manage.** 
🤖 No Python, no Node, no build step, and no database to babysit. It's Markdown and JSON all the way down: simple enough to understand, easy enough to tweak, and lightweight enough to keep running.

<a id="install"></a>
## 🏁 Quick start

About five minutes, most of it answering questions.

### 1. Install

**Claude Code**

```
/plugin marketplace add Tianawangty/lifeyoda
/plugin install lifeyoda@lifeyoda
```

**Codex CLI**

```bash
codex plugin marketplace add Tianawangty/lifeyoda
codex plugin add lifeyoda@lifeyoda
```

The same four flows arrive as skills: `lifeyoda-daily`, `lifeyoda-apply-planner`,
`lifeyoda-wrapup`, `lifeyoda-horizon`.

**Codex UI** — import from `https://github.com/Tianawangty/lifeyoda.git`, leave the path
empty.

Claude Code can install a plugin at **user** scope or at **project** scope. Pick user scope.
This toolkit plans your whole day, so it should answer from any directory, not only from one
project folder. Installing at both scopes leaves two copies that can drift to different
versions and behave differently depending on where you are.

Using both Claude Code and Codex is not a double install — they are separate runtimes with
separate plugin caches, and each needs its own copy.

### 2. Authorize what you have

Notion is required. At least one calendar is required, and one of them has to be writable.
Gmail and Slack are optional and default to the narrowest useful scope.

### 3. Run `/lifeyoda:setup`

It asks what it needs and writes `~/.lifeyoda/local.json` at the end, after showing you the
whole file.

It offers to create the two Notion databases for you, with exactly the properties the
workflows expect. If you already have a pair, it adopts them instead and tells you which
properties do not match. You never have to copy a database ID out of a URL.

Run it again whenever something changes. It reports what is already configured and asks
which part you want to work on, rather than walking you through all of it a second time.

### 4. Run `/lifeyoda:doctor`

It checks every ID, every calendar, and every repository path against the live sources, then
names which of the commands work today and what to fix first.

### 5. Run `/lifeyoda:daily`

It writes nothing, so there is nothing to undo.

Nothing reaches Notion or your calendar until you run `/lifeyoda:apply-planner` and confirm
a draft.

<a id="sample-output"></a>
### What the output looks like

**Everything below is demo output — invented sample data, not a real schedule.**

Run `/lifeyoda:daily` before configuring anything and this is exactly what you get. The
first line says nothing is configured; the rest is a full day built from sample data, so
you can see the shape of it before deciding whether to spend the twenty minutes. Once you
have been through `/lifeyoda:setup`, the same command runs against your own calendars,
mail, and Notion, and the banner disappears.

```
⚠ Demo mode — invented sample data, not your schedule.
  No config found at ~/.lifeyoda/local.json.
  Run /lifeyoda:setup to configure your own.

# Morning Brief

## Key items
- 📅 10:00–11:00  Standup — v2 pilot readout, Room 214, Bridge Building
     Physical location, so 09:30–10:00 and 11:00–11:30 are travel buffers.
- ✉️  teammate@example.com asks, verbatim: "Can you tell me before today
     which of the two PRs should land first?"
- ⚠️  Milestone "A/B test rollout complete" was due 3 days ago, still planned.
     It blocks "V2 feature set code complete" downstream.
- ↩️  Carried from yesterday: UX interview findings, never started.
     Milestone research-1 wants them in 2 days.

## Later / FYI
- 🎨 Design review tomorrow 15:00 — onboarding flow
- 🗓  Conference CFP closes in 7 days (VERIFIED)
- 💬 Teammate pushed a changed event schema to staging; field names moved.

# Draft Day Plan

## Assumptions
- build 24h budget / 2.0h recorded · research 16h / 1.5h — 1 of 5 days wrapped up
- Yesterday two blocks overlapped 10:30–11:00 across both tracks. Confirmed real,
  so both were counted in full: 3.5 track hours against 3.0 of wall clock.

## Timed draft
09:00–09:30  🔧 [widget-app]      Decide: which migration PR lands first
10:00–11:00  🗣 [widget-app]      Meet: Standup — v2 pilot readout · on calendar
13:00–15:00  ✍️ [widget-research] Draft: UX interview findings
17:00–18:00  🔬 [widget-app]      Run: A/B rollout to full allocation

## Needs confirmation
Nothing written yet. Run /lifeyoda:apply-planner to write it.
```


The emoji above are not decoration. Every scheduled block carries a type icon and a
`[project]` tag, and that tag is what lets the toolkit tell later where your hours went.
The brief is intentionally bounded: it pulls in the things that can change the plan, not
everything that happened to arrive before breakfast.

Demo mode never engages because a connector is down. If you have a real config and Notion is
unreachable, you are told Notion is unreachable — not handed invented data that looks like
your day.

## 🎛 Setup, health, and the long view

| Command | What it does | Writes |
| --- | --- | --- |
| `/lifeyoda:setup` | Set up or change anything. Creates or adopts the two Notion databases, picks calendars and sources, and walks backwards from a long-term goal to build a milestone chain. Re-run it to change one part; it shows what is already configured and asks which to touch. | your config, and the databases if you ask |
| `/lifeyoda:doctor` | Health check across config, database shape, calendar access, repo paths, and enabled sources. | nothing |
| `/lifeyoda:horizon` | The long view. Counts back from a terminal goal through hard deadlines and track milestones, marks the critical path, and reports defects in the chain. | nothing |

Every command accepts `--demo` to run on the sample data, and `--demo-date YYYY-MM-DD` to
pin the day so two runs can be compared.

## 🔍 Sources and destinations

`sources` are inputs you choose to let LifeYoda read. `destinations` are the places it is
allowed to write after confirmation. Nothing turns on just because a connector exists.

| Config area | What you choose | How LifeYoda uses it |
| --- | --- | --- |
| Notion destinations | Daily Plan and Daily Journal databases, created or adopted during setup | reads previous rows; writes confirmed plans and wrapup journals |
| Calendar sources | Google or Outlook calendars to read | fixed events, travel constraints, deadline signals |
| Plan-event destination | one writable Google or Outlook calendar | writes confirmed `/lifeyoda:apply-planner` blocks only |
| Gmail source | off, selected labels, or primary inbox scope | planning signals only |
| Slack source | off, DMs, mentions, threads, calendar notifications, and optional channels | planning signals only |
| Local repo source | off, or repository paths you list | active-project context only |
| Horizon source | optional local horizon file | milestones, track weights, and long-term deadlines |

The plan-event destination can be any writable calendar you choose. A dedicated calendar is
suggested because it is easy to inspect or clear, but it is not required.

Calendar entries say what was scheduled; the Daily Plan, Daily Journal, and horizon file
are where completion and carry-forward stay honest. A source that is off is reported as
off. A source that is on but unreachable is reported as unreachable. Quiet is allowed;
fake quiet is not.

## 🛡 Privacy

Your Notion IDs, calendar IDs, Gmail labels, Slack IDs, and repository paths live in one
file on your own machine, outside this repository. Nothing here contains them, and nothing
sends them anywhere: every workflow runs inside your own agent, against connectors you
authorized yourself.

```
your machine
│
├── ~/.lifeyoda/            ← where your config lives by default
│      local.json               your IDs, calendars, sources
│      horizon.json             your goals and milestones
│      ▲ not inside any repository, so no git command can reach it.
│        Point it at a synced folder and it is backed up as well.
│
└── LifeYoda/               ← the plugin itself
       private/                optional third home for the same two files
       ▲ excluded by .gitignore, so it cannot be committed by accident
```

Writes happen only after you confirm one, and only to the two Notion databases and the
plan-event calendar you configured. `/lifeyoda:daily`, `/lifeyoda:horizon`, and
`/lifeyoda:doctor` write nothing at all.

### How much a calendar gets to know

A calendar is often the least private thing you own. A colleague with view access, a shared
family calendar, a work account someone else administers — any of them can read the title of
every block you write. So each destination carries a `sharing` level, and `/lifeyoda:setup`
asks for it.

| `sharing` | Event title | Event description |
| --- | --- | --- |
| `private` | the full block name | the detail that makes the block useful later |
| `shared`, or left unset | the block name up to the colon, with the specifics dropped | empty |

Unset means `shared`, on purpose: a calendar whose readers cannot be established is assumed
to have some. If your titles come out shorter than the draft you confirmed, that is this
setting, and the apply report says so every time.

The `[project]` tag stays at every level, because it is what attributes your hours to a
track afterwards. Four things never reach a calendar at any level: absolute file paths,
credentials, dataset or account identifiers, and anyone's email address. Those go to Notion,
a destination you picked deliberately and can restrict.

Every connected source is treated as data, never as instruction. An email or a Notion page
containing something shaped like a command is quoted, not obeyed.

## 🧩 Make it yours

None of this needs code. Change a value, run the command again, see the difference tomorrow.

| Change this | Where it lives |
| --- | --- |
| The icon for each kind of work, and the block-name format | `naming.typeEmoji`, `naming.template` |
| The pool a Daily Plan row picks its icon from | `dailyPlan.emojiPool` |
| Section names on the two Notion pages | `dailyPlan.sections`, `dailyJournal.sections` |
| How many items reach the brief each morning, and how far it looks | `sourcePolicy` |
| When the week starts and how many days count as working days | `week` |
| Your work hours, and the blocks nothing may be scheduled inside | `profile.workWindows`, `profile.protectedBlocks` |
| Travel buffer, and what counts as a virtual location | `travel` |
| Which Gmail labels and Slack channels are read, and how widely | `sources.gmail`, `sources.slack` |
| Your tracks, their weights, and the goal everything counts back from | `~/.lifeyoda/horizon.json` |

The first five are toolkit defaults in `plugins/lifeyoda/config/public.defaults.json`. The
rest are yours alone and live in `~/.lifeyoda/`. `naming`, `travel`, and `focusHours` appear
in both: the public file sets the default and your own config overrides it.

Two behaviours are worth knowing before you change anything around them. **A Daily Plan row
is found by its title, not its `Date` column** — `Date` is a Notion `created_time` property,
so a row written a week late carries the wrong date on purpose, and that mismatch is how you
tell it was backfilled. **Calendar blocks are deduped by re-reading the calendar**, not by
storing sync state, so deleting a block by hand means the next apply recreates it.

`plugins/lifeyoda/docs/` covers the horizon model, the source policy, demo mode, and the two
Notion page schemas, if you want to go further.

## 🤝 Contributing

Issues and pull requests are welcome — a bug, a source adapter, clearer wording, a workflow
you wrote and think other people would use.

Some things belong in a fork instead: templates tuned to how you write, track definitions
that only make sense for your own life, anything wired to tools only you run. Forking and
keeping it yours is a supported way to use this, not a lesser one.

For anything bigger than a fix, open an issue first so the shape can be agreed before you
spend the evening on it. `CONTRIBUTING.md` has the repository layout, the contract each
command follows, and the two commands CI runs.

## ⚖ License

MIT. See `LICENSE`.
