# CLAUDE.md

Claude Code specifics for this repository. **Read `CONTRIBUTING.md` first** — it carries
the repository layout, the command loop, config resolution, the four non-obvious facts
about the Notion/calendar model, the naming protocol, and the read-only boundaries.
Nothing in that file is repeated here.

`AGENTS.md` is the Codex counterpart to this file.

## Command surface

Claude Code enters through `plugins/lifeyoda/commands/*.md`. Installed, the commands are
namespaced. The core daily loop is four commands:

```
/lifeyoda:daily          Morning Brief + Draft Day Plan   (read-only)
/lifeyoda:apply-planner  write the confirmed plan
/lifeyoda:wrapup         reconcile and journal
/lifeyoda:horizon        long-horizon view                (read-only)
```

Two supporting commands stay outside that loop:

```
/lifeyoda:setup          create/adopt databases, choose sources, write config
/lifeyoda:doctor         validate config, database shape, calendars, sources
```

This mirrors `AGENTS.md` by role, not by exact entry syntax. The shared product facts
belong in `CONTRIBUTING.md`; this file only records what is different about Claude Code.

There is no unnamespaced source-checkout command surface. Working on this repository means
installing the plugin like any other user, which is what keeps the install path honest —
a broken install shows up the same day rather than weeks later.

## Locating packaged files

Command files address packaged files through `${CLAUDE_PLUGIN_ROOT}`:

```
${CLAUDE_PLUGIN_ROOT}/workflows/morning-brief-and-plan.md
${CLAUDE_PLUGIN_ROOT}/config/public.defaults.json
```

Each command also carries a fallback for the case where it has been migrated into a Codex
skill, expressed relative to the skill's own directory (`../../workflows/…`). A skill sits
at `<plugin>/codex-skills/<name>/`, so the correct depth is two levels, not three. A wrong depth
here fails silently: the read simply finds nothing.

## Installs are keyed on the plugin version

The cache directory is named after the version
(`~/.claude/plugins/cache/lifeyoda/lifeyoda/<version>/`), and an install at a version
already present is skipped without a word. `/plugin marketplace update` refreshes
marketplace metadata only, not the installed plugin.

So any change under `plugins/lifeyoda/` needs the version bumped, or Claude Code keeps
running the old text. Four files must agree:

- `plugins/lifeyoda/.claude-plugin/plugin.json`
- `plugins/lifeyoda/.codex-plugin/plugin.json`
- `.claude-plugin/marketplace.json` (two lines)
- `plugins/lifeyoda/config/public.defaults.json`

`scripts/check.py` enforces this. Codex does not have the problem —
`.agents/plugins/marketplace.json` pins no version and `codex plugin add` re-copies
unconditionally.

## Marketplace surface

`.claude-plugin/marketplace.json` declares the marketplace and points at
`./plugins/lifeyoda`. Install:

```
/plugin marketplace add Tianawangty/lifeyoda
/plugin install lifeyoda@lifeyoda
```

A marketplace added from a local directory registers as `"source": "directory"` in
`~/.claude/plugins/known_marketplaces.json`. That is a different code path from the GitHub
install above, so a local install proves nothing about whether the published one works.

## Shell environment

Claude Code's Bash tool runs a **non-interactive login zsh**. It reads `~/.zshenv` and
`~/.zprofile` and never sources `~/.zshrc`. Any environment variable a workflow depends on
— including a `$VAR` used as a repo `localPath` — must therefore be defined in `.zshenv`.
