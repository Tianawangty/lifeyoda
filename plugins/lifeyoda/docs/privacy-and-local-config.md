# Privacy and Local Config

Nothing that identifies you belongs in this repository. The toolkit is split so that
the two never mix: public files carry schemas, placeholders, and behaviour; a private
layer carries your actual IDs and paths.

## Where the private layer lives

Every workflow resolves it in this order, first hit wins:

1. `$LIFEYODA_CONFIG/local.json`
2. `~/.lifeyoda/local.json`
3. `private/local.json`, only when running from a source checkout

All three tiers are supported equally. `~/.lifeyoda/` is the one to use with an installed
plugin, since it resolves from any working directory — it can be a real directory or a
symlink into a synced folder that sits outside any git repository. Tier 3 resolves only
when the working directory is the checkout, and it is gitignored and untracked, so
`git clean -xdf` deletes it and a fresh clone starts with nothing.

Never edit the installed plugin cache. Your edits there are silently discarded on the
next install.

## What is private

Anything that identifies a person, account, workspace, course, repository, database,
document, or schedule:

- Notion database IDs, data source URLs, and block IDs
- Calendar IDs, including the planning calendar you write to
- Gmail label IDs; Slack channel and DM IDs
- Local repository paths, and the GitHub repos you point at
- Checklist source locators

A repo path may be written as a single `$VAR` instead of a literal path. That form exists
so a path embedding personal data — an account email inside a cloud-storage folder name,
for example — never enters a config file at all. Set those variables in `~/.zshenv`, not
`~/.zshrc`: the agent runtimes read `.zshenv` and never source `.zshrc`.

## What is public

Schemas, placeholder examples, naming rules, section names, and workflow prose.
`private.example/` mirrors the private layer's shape with placeholders only.

## The rule for anything new

When adding a field, decide first whether its value is public design or private user
data. If it names a person, account, workspace, class, repo, database, document, or
schedule, it goes in the private layer and the public example gets a placeholder.
