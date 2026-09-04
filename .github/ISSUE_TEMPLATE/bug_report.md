---
name: Bug report
about: Something behaved differently from what the workflow says it should
labels: bug
---

**Never paste real IDs.** Calendar IDs, Notion database IDs and `collection://` URLs, Gmail
label IDs, Slack channel and DM IDs, and absolute home paths all identify you. Replace them
with placeholders such as `<calendar-id>`.

### Which command

`/lifeyoda:daily` · `/lifeyoda:apply-planner` · `/lifeyoda:wrapup` · `/lifeyoda:horizon` ·
`/lifeyoda:setup` · `/lifeyoda:doctor`

### Runtime

Claude Code · Codex CLI · Codex UI — and the plugin version from `plugin.json`.

### What happened, and what the workflow says should happen

Quote the line from the workflow file if you can find it. "It should be smarter" is hard to
act on; "`workflows/wrapup-journal.md` says the icon is `✅` when every item is checked, and
I got `📓`" is a bug report.

### `/lifeyoda:doctor` output

Paste it with IDs redacted. It reports config tier, Notion database shape, calendar access,
and repository paths, which is most of what a diagnosis needs.

### Does it reproduce in demo mode?

Run the command with `--demo`. Demo mode uses fixed synthetic fixtures, so a bug that
reproduces there is one anyone can see, and one that does not points at configuration.
