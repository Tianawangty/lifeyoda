# Public release checklist

What still stands between this repository and a public release, and what has already been
measured so it does not have to be measured again.

Nothing here is a blocker on day-to-day use. The repository works as a private toolkit
today; this file exists so that the decision to publish is made against facts rather than
against a vague sense that something personal might be in there.

## What was measured

Run on 2026-08-31 against the tracked tree and the packaged plugin.

| Scan | Result |
| --- | --- |
| Account email, phone, and alternate-address patterns, tracked tree | zero hits |
| Same patterns, packaged plugin | zero hits |
| Employer and collaborator names, tracked tree | zero hits |
| Notion database and data-source IDs, tracked tree | zero hits |
| Calendar IDs, tracked tree | zero hits |
| Absolute paths under a home directory, whole repository | zero hits |
| Commit messages across all 13 commits | zero hits on identifying terms |
| Files tracked under `private/` | `.gitkeep` only |

The commit author is a GitHub `users.noreply.github.com` address, which is what that
address form is for: it identifies the author without publishing an email.

Reproduce all of it with the three checks in `CLAUDE.md` under "Verify config health",
plus:

```bash
git log --all --format='%an <%ae> %s'      # author identity and every commit subject
grep -rnI --exclude-dir=.git -E "/Users/[a-zA-Z]+/" .
```

## What is not personal but still needs a decision

**The license contradicts itself.** `LICENSE` says no open-source license has been
selected. Both `plugins/lifeyoda/.claude-plugin/plugin.json` and
`plugins/lifeyoda/.codex-plugin/plugin.json` declare `"license": "Proprietary"`. Either
statement alone forbids public reuse, and they do not agree with each other. Publishing
without resolving this ships a package nobody may legally use. Pick one license, then make
all three files say it.

**The connector IDs in `.app.json` are unverified.** The file names five app and connector
IDs — Notion, Gmail, Slack, Google Calendar, GitHub. They look like platform-level
identifiers rather than account tokens, and the Notion one matches the ID in the local
Codex config, which is consistent with a shared global ID. That is inference, not
verification. Confirm against the platform's own documentation that these are stable public
IDs before publishing, and confirm that installing a plugin which references them grants no
account access on its own.

**`CLAUDE.md` and `AGENTS.md` carry development context, not personal data.** They point at
`private/NOTES.md`, describe a local editor hook, and record decisions in the first person
about how this repository is worked on. No scan finds anything identifying in them. They
simply read as one person's working notes, which is a presentation question rather than a
privacy one — and which route you take below decides whether it matters at all.

## Two routes, and what each costs

**Route A — flip this repository to public.**

Viable, because the history is clean. It costs the working notes: `CLAUDE.md` and
`AGENTS.md` would have to be rewritten for an outside reader, and every future edit to them
becomes a publishing decision. The repository stops being a place to write freely.

Steps: resolve the license across all three files, rewrite the two agent-instruction files
for an outside audience, verify the connector IDs, merge `dev` to `main`, install from
`main` and confirm the four commands run.

**Route B — export the package to a separate public repository.**

`plugins/lifeyoda/` is already self-contained: it carries its own `config/`, `docs/`,
`workflows/`, `templates/`, `commands/`, `skills/`, and `private.example/`. Publishing it
as the root of a second repository leaves this one private and unconstrained, so the
working notes stay working notes.

Steps: resolve the license inside the package, verify the connector IDs, write a README
addressed to someone who has never seen this repository, create the public repository from
the package contents, and add an export step to the release process so the two do not
drift.

Neither route is chosen yet.

## Before either route

- Synthetic dry-run fixtures with privacy assertions, so a release can be tested without
  anyone's real Notion workspace. Note that adding them changes what this repository is:
  it currently contains no executable code at all, which is a property worth keeping
  deliberately rather than losing by accident.
- Verify a clean install end to end from whichever repository publishes, on a machine
  where no private config exists, and confirm the workflows report missing config instead
  of inventing sources.
