# AGENTS.md

Codex specifics for this repository. **Read `CONTRIBUTING.md` first** — it carries the
repository layout, the command loop, config resolution, the four non-obvious facts about
the Notion/calendar model, the naming protocol, and the read-only boundaries. Nothing in
that file is repeated here.

`CLAUDE.md` is the Claude Code counterpart to this file.

## Skill surface

Codex enters through `plugins/lifeyoda/skills/*/SKILL.md`. The core daily loop is four
skills:

```
lifeyoda-daily           Morning Brief + Draft Day Plan   (read-only)
lifeyoda-apply-planner   write the confirmed plan
lifeyoda-wrapup          reconcile and journal
lifeyoda-horizon         long-horizon view                (read-only)
```

Two supporting skills stay outside that loop:

```
lifeyoda-setup           create/adopt databases, choose sources, write config
lifeyoda-doctor          validate config, database shape, calendars, sources
```

This mirrors `CLAUDE.md` by role, not by exact command syntax. The shared product facts
belong in `CONTRIBUTING.md`; this file only records what is different about Codex.

A `SKILL.md` carries `name` and `description` in its frontmatter and locates packaged
files relative to its own directory:

```
../../workflows/morning-brief-and-plan.md
../../config/public.defaults.json
```

A skill sits at `<plugin>/skills/<name>/`, so packaged files are exactly two levels up.
Getting the depth wrong fails silently — the read finds nothing rather than erroring.

## Manifest

`plugins/lifeyoda/.codex-plugin/plugin.json` points `skills` at `./skills/` and `apps` at
`./.app.json`. It also carries an `interface` block that Codex renders directly:
`displayName`, `shortDescription`, `longDescription`, `developerName`, `category`,
`capabilities` (`Interactive`, `Read`, `Write`), three `defaultPrompt` strings, and
`brandColor`. Changing the user-facing name or blurb means editing that block, not the
top-level `description`.

## Connectors

`plugins/lifeyoda/.app.json` declares six connectors — Notion, Gmail, Slack, Google
Calendar, Outlook Calendar, GitHub — all `"required": false`, so an install succeeds
without any of them and an unavailable source is reported rather than guessed at. The
marketplace entry sets `"authentication": "ON_INSTALL"`, which is what prompts for
authorization at install time.

Every id there is a platform binding for a connector *type*, portable across workspaces.
None of them identifies an account, a workspace, or a particular authorization.

`"required": false` on every entry is deliberate: an unavailable source is reported rather
than guessed at, and demo mode has to run with nothing connected at all.

Claude Code has no equivalent declaration, so a Claude Code user is never prompted to
connect anything — the setup guidance has to tell them.

## Marketplace surface

`.agents/plugins/marketplace.json` declares the Codex marketplace and points at
`./plugins/lifeyoda`. Install:

```bash
codex plugin marketplace add Tianawangty/lifeyoda
codex plugin add lifeyoda@lifeyoda
```

For a Codex UI workspace import, use source `https://github.com/Tianawangty/lifeyoda.git`
and leave the path empty.

Unlike Claude Code, Codex pins no version in the marketplace manifest and `codex plugin
add` re-copies unconditionally, so a Codex install always picks up the current contents.
The installed cache lives at `~/.codex/plugins/cache/lifeyoda/lifeyoda/<version>/`, and a
marketplace added from a local directory registers as `source_type = "local"` in
`~/.codex/config.toml` — a different code path from the GitHub install above.

## Shell environment

Codex ships its own zsh and reads `~/.zshenv` on every invocation. Any environment
variable a workflow depends on — including a `$VAR` used as a repo `localPath` — belongs
there rather than in `~/.zshrc`.
